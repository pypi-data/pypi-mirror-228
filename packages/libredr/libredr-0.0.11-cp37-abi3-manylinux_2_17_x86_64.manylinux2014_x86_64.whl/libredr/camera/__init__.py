'''
All camera models (python)
'''
__all__ = ["look_at_extrinsic", "orthogonal_ray", "perspective_ray", "cube_ray"]

import numpy as np

# Camera model use x-right, y-down, z-forward axis scheme

# Orthogonal camera model
from .orthogonal import orthogonal_ray
# Perspective camera model
from .perspective import perspective_ray
# Cubic unwrapped panorama camera model
from .cube import cube_ray

def look_at_extrinsic(position, look_at, up):
  '''
  Construct 4 * 4 extrinsic matrix from `position`, `look_at`, `up` vectors
  '''
  d = look_at - position
  assert(np.linalg.norm(d) > 1e-6)
  d = d / np.linalg.norm(d)
  right = np.cross(d, up)
  assert(np.linalg.norm(right) > 1e-6)
  right = right / np.linalg.norm(right)
  down = np.cross(d, right)
  return np.array([
    [right[0], right[1], right[2], 0.],
    [down[0], down[1], down[2], 0.],
    [d[0], d[1], d[2], 0.],
    [0., 0., 0., 1.]
  ], dtype=np.float32).dot(np.array([
    [1., 0., 0., -position[0]],
    [0., 1., 0., -position[1]],
    [0., 0., 1., -position[2]],
    [0., 0., 0., 1.],
  ], dtype=np.float32))
