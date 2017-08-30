import request from '../utils/request';

export function getStorage({ page, pageSize }) {
  return request(`manager/basic_setting/storage/all?page=${page}&&paginate_by=${pageSize}`);
}

export function addStorage(data) {
  return request({
    method: 'PUT',
    url: 'manager/basic_setting/storage',
    data,
  });
}

export function editStorage(data) {
  console.log(data)
  return request({
    method: 'POST',
    url: 'manager/basic_setting/storage',
    data,
  });
}
