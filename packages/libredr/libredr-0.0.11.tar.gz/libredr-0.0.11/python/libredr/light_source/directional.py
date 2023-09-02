import math
import numpy as np

def directional_envmap(resolution, direction, intensity):
  '''
  Construct one-hot envmap with given direction and intensity
  # Arguments
  * `resolution`: a single integer
  * `direction`: float vector of 3
  * `intensity`: float scalar
  # Return
  * 3 * 6 * `resolution` * `resolution`
  '''
  direction_abs = np.abs(direction)
  if direction_abs[0] > direction_abs[1]:
    if direction_abs[0] > direction_abs[2]:
      face_id = 0
    else:
      face_id = 2
  else:
    if direction_abs[1] > direction_abs[2]:
      face_id = 1
    else:
      face_id = 2
  direction = direction / direction_abs[face_id]
  if face_id == 0:
    uv = np.array([direction[1], direction[2]], dtype=np.float32)
  elif face_id == 1:
    uv = np.array([direction[0], direction[2]], dtype=np.float32)
  else:
    uv = np.array([direction[0], direction[1]], dtype=np.float32)
  uv = np.clip((uv + np.float32(1.0)) / np.float32(2.0), np.float32(1e-6), np.float32(1.0 - 1e-6))
  envmap_col = math.floor(uv[0] * resolution)
  envmap_row = resolution - 1 - math.floor(uv[1] * resolution)
  if direction[face_id] < 0:
    face_id = face_id * 2 + 1
  else:
    face_id = face_id * 2
  envmap = np.zeros([3, 6, resolution, resolution], dtype=np.float32)
  intensity = intensity * np.power(resolution, 2) * np.power(np.linalg.norm(direction, ord=2), 3)
  envmap[:, face_id, envmap_row, envmap_col] = intensity
  return envmap
