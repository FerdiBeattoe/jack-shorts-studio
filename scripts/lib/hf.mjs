/**
 * Shared HuggingFace helpers used by hf-upload-dataset.mjs and hf-upload-lora.mjs.
 *
 * Lazy-loads @huggingface/hub so a missing dep produces a clear `npm install`
 * message rather than a confusing import error.
 */

let hfModulePromise = null;
async function loadHfHub() {
  if (!hfModulePromise) {
    hfModulePromise = import("@huggingface/hub").catch((err) => {
      console.error("ERROR: `@huggingface/hub` package not installed.");
      console.error("Run: npm install");
      throw err;
    });
  }
  return hfModulePromise;
}

/**
 * Find the highest existing version for repos matching `{username}/{prefix}-v{N}`.
 * Returns 0 if no matching repos exist.
 */
export async function latestVersion({ repoType, username, prefix, accessToken }) {
  const hub = await loadHfHub();
  const list = repoType === "dataset" ? hub.listDatasets : hub.listModels;
  const re = new RegExp(`^${escapeRegExp(username)}/${escapeRegExp(prefix)}-v(\\d+)$`);
  let max = 0;
  try {
    for await (const repo of list({ search: { owner: username }, credentials: { accessToken } })) {
      const m = (repo.name || repo.id || "").match(re);
      if (m) {
        const n = Number(m[1]);
        if (Number.isFinite(n) && n > max) max = n;
      }
    }
  } catch (err) {
    console.warn(`WARN: could not list ${repoType} repos for ${username}: ${err.message}`);
  }
  return max;
}

/**
 * Find the next free version number for repos matching `{username}/{prefix}-v{N}`.
 *
 * @param {object} opts
 * @param {"dataset"|"model"} opts.repoType
 * @param {string} opts.username
 * @param {string} opts.prefix         e.g. "jack-saas-training" or "jack-saas-lora"
 * @param {string} opts.accessToken
 * @returns {Promise<number>}          next version (1 if no existing repos)
 */
export async function nextVersion({ repoType, username, prefix, accessToken }) {
  return (await latestVersion({ repoType, username, prefix, accessToken })) + 1;
}

/**
 * Create a repo if it doesn't already exist. No-op if it does.
 */
export async function ensureRepo({ repoType, name, accessToken, isPrivate = true }) {
  const hub = await loadHfHub();
  try {
    await hub.createRepo({
      repo: { type: repoType, name },
      credentials: { accessToken },
      private: isPrivate,
    });
    return { created: true };
  } catch (err) {
    const msg = String(err?.message || err);
    if (err?.statusCode === 409 || /already.*(exist|created)|409/i.test(msg)) return { created: false };
    throw err;
  }
}

/**
 * Upload a single file to a repo at a given path-in-repo.
 */
export async function uploadOneFile({ repoType, name, accessToken, localPath, pathInRepo }) {
  const hub = await loadHfHub();
  const { readFileSync, statSync } = await import("node:fs");
  const size = statSync(localPath).size;
  const content = new Blob([readFileSync(localPath)]);
  await hub.uploadFile({
    repo: { type: repoType, name },
    credentials: { accessToken },
    file: {
      path: pathInRepo,
      content,
      size,
    },
  });
}

function escapeRegExp(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

/**
 * Check whether a file exists in a HuggingFace repo via HEAD on the resolve URL.
 * Works for both public and private repos (private needs an accessToken).
 *
 * @param {object} opts
 * @param {"model"|"dataset"|"space"} opts.repoType
 * @param {string} opts.name              e.g. "user/jack-saas-lora-v3"
 * @param {string} opts.pathInRepo        e.g. "jack-lora.safetensors"
 * @param {string} [opts.revision="main"]
 * @param {string} [opts.accessToken]
 * @returns {Promise<boolean>}
 */
export async function fileExists({ repoType, name, pathInRepo, revision = "main", accessToken }) {
  const prefix = repoType === "dataset" ? "datasets/" : repoType === "space" ? "spaces/" : "";
  const url = `https://huggingface.co/${prefix}${name}/resolve/${revision}/${pathInRepo}`;
  const headers = accessToken ? { Authorization: `Bearer ${accessToken}` } : {};
  try {
    const res = await fetch(url, { method: "HEAD", headers, redirect: "follow" });
    return res.ok;
  } catch {
    return false;
  }
}
