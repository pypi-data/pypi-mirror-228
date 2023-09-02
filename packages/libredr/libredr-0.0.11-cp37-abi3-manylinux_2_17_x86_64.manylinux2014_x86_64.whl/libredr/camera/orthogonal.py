import numpy as np

def orthogonal_ray(resolution, intrinsic, extrinsic):
  '''
  Construct input ray for orthogonal camera model
  # Arguments
  * `resolution`: tuple of 2 integers [`width`, `height`]
  * `intrinsic`: 3 * 3 matrix
  * `extrinsic`: 4 * 4 matrix
  # Return
  * 18 * `height` * `width`
  Camera model use x-right, y-down, z-forward axis scheme
  '''
  intrinsic_inv = np.linalg.inv(intrinsic)
  extrinsic_inv = np.linalg.inv(extrinsic)
  axis_x = np.linspace(
	  0.5 - 0.5 * resolution[0] / max(*resolution),
    0.5 + 0.5 * resolution[0] / max(*resolution),
    resolution[0] + 1, dtype=np.float32)[:, np.newaxis]
  axis_y = np.linspace(
    0.5 - 0.5 * resolution[1] / max(*resolution),
    0.5 + 0.5 * resolution[1] / max(*resolution),
    resolution[1] + 1, dtype=np.float32)[np.newaxis,:]
  axis_z = np.array([[1.0]], dtype=np.float32)
  axis_xyz = np.stack(np.broadcast_arrays(axis_x, axis_y, axis_z), axis=-1)
  axis_xyz = np.matmul(intrinsic_inv, axis_xyz[..., np.newaxis]).squeeze(-1)
  axis_xyz = np.broadcast_arrays(axis_xyz[..., 0], axis_xyz[..., 1], np.float32(0.0), np.float32(1.0))
  axis_xyz = np.stack(axis_xyz, axis=-1)[..., np.newaxis]
  ret_r = np.matmul(extrinsic_inv, axis_xyz).squeeze(-1)[..., :3]
  ret_r = np.concatenate([ret_r[:-1,:-1, ...],
    ret_r[:-1, 1:, ...] - ret_r[:-1,:-1, ...],
    ret_r[1:,:-1, ...] - ret_r[:-1,:-1, ...]], axis=-1)
  ret_r = ret_r.transpose(2, 1, 0)
  ret_rd = np.array([0.0, 0.0, 1.0], dtype=np.float32)[:, np.newaxis]
  ret_rd = np.matmul(extrinsic_inv[:3,:3], ret_rd)[..., np.newaxis]
  ret_rd = np.broadcast_to(ret_rd, (3, resolution[1], resolution[0]))
  ret_rd = np.concatenate(np.broadcast_arrays(ret_rd, np.float32(0.0), np.float32(0.0)), axis=0)
  return np.concatenate([ret_r, ret_rd], axis=0)
