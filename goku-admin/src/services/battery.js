import request from '../utils/request';

export function getAllBattery({ page, pageSize }) {
  return request(`manager/battery_setting/battery/all?page=${page}&paginate_by=${pageSize}`);
}

export function getBatteryRecord(days) {
  return request(`manager/battery_setting/history_record?days=${days}`);
}

export function getBatteryReport() {
  return request('manager/support/battery_report/all');
}
