/**
 * Minimal RunPod REST API client (https://rest.runpod.io/v1).
 *
 * Wraps the four endpoints we need for orchestrated training:
 *   - createPod    POST   /pods
 *   - getPod       GET    /pods/{id}
 *   - terminatePod DELETE /pods/{id}
 *   - listGpuTypes GET    /gpuTypes   (diagnostic, used by --list-gpus)
 *
 * RunPod's API surface has shifted between v1-graphql and v1-rest over time.
 * If a call 4xx's with an unexpected schema error, hit
 *   https://docs.runpod.io/api-reference
 * and adjust the request shape — the network calls are localized to this file.
 */

const BASE = process.env.RUNPOD_API_BASE || "https://rest.runpod.io/v1";

function authHeaders(apiKey) {
  return {
    Authorization: `Bearer ${apiKey}`,
    "Content-Type": "application/json",
    Accept: "application/json",
  };
}

async function request({ apiKey, method, path, body }) {
  const url = `${BASE}${path}`;
  const res = await fetch(url, {
    method,
    headers: authHeaders(apiKey),
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });

  const text = await res.text();
  let json;
  try {
    json = text ? JSON.parse(text) : null;
  } catch {
    json = { _raw: text };
  }

  if (!res.ok) {
    const detail = json?.error?.message || json?.message || json?._raw || res.statusText;
    const err = new Error(`RunPod ${method} ${path} → HTTP ${res.status}: ${detail}`);
    err.status = res.status;
    err.body = json;
    throw err;
  }
  return json;
}

/**
 * Create a pod.
 *
 * @param {object} opts
 * @param {string} opts.apiKey
 * @param {string} opts.name
 * @param {string} opts.imageName               container image (e.g. PyTorch template)
 * @param {string[]} opts.gpuTypeIds            RunPod GPU type IDs (e.g. ["NVIDIA GeForce RTX 4090"])
 * @param {"SECURE"|"COMMUNITY"} [opts.cloudType="SECURE"]
 * @param {number} [opts.gpuCount=1]
 * @param {number} [opts.containerDiskInGb=60]
 * @param {number} [opts.volumeInGb=0]
 * @param {string} [opts.volumeMountPath="/workspace"]
 * @param {Array<{key:string,value:string}>} [opts.env=[]]
 * @param {string} [opts.dockerArgs]            container CMD override
 * @param {string} [opts.ports]                 e.g. "22/tcp" — none needed for our flow
 * @param {boolean} [opts.supportPublicIp=false]
 */
export async function createPod(opts) {
  const body = {
    name: opts.name,
    imageName: opts.imageName,
    gpuTypeIds: opts.gpuTypeIds,
    cloudType: opts.cloudType || "SECURE",
    gpuCount: opts.gpuCount ?? 1,
    containerDiskInGb: opts.containerDiskInGb ?? 60,
    volumeInGb: opts.volumeInGb ?? 0,
    volumeMountPath: opts.volumeMountPath || "/workspace",
    env: opts.env || [],
    dockerArgs: opts.dockerArgs,
    ports: opts.ports,
    supportPublicIp: opts.supportPublicIp ?? false,
  };
  return request({ apiKey: opts.apiKey, method: "POST", path: "/pods", body });
}

export async function getPod({ apiKey, id }) {
  return request({ apiKey, method: "GET", path: `/pods/${encodeURIComponent(id)}` });
}

export async function terminatePod({ apiKey, id }) {
  return request({ apiKey, method: "DELETE", path: `/pods/${encodeURIComponent(id)}` });
}

export async function listGpuTypes({ apiKey }) {
  return request({ apiKey, method: "GET", path: "/gpuTypes" });
}
