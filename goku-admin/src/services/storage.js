import request from '../utils/request';

export function getStorage({ page, pageSize }) {
  return request(`manager/basic_setting/storage/all?page=${page}&&paginate_by=${pageSize}`);
}
