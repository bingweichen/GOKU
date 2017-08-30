import request from '../utils/request';

export function getAllBattery({ page, pageSize, keyWord }) {
  let url = `manager/battery_setting/battery/all?page=${page}&paginate_by=${pageSize}`;
  url = keyWord ? `${url}&serial_number=${keyWord}` : url;
  return request(url);
}

export function getBatteryRecord(days, keyWord, page, pageSize) {
  let url = `manager/battery_setting/history_record?days=${days}&page=${page}&paginate_by=${pageSize}`;
  url = keyWord ? `${url}&serial_number=${keyWord}` : url;
  return request(url);
}

export function getBatteryReport() {
  return request('manager/support/battery_report/all');
}

// 使用闪充的总人次
export function getTotalUse() {
  return request('manager/battery_setting/total_use');
}

// 正在使用人数
export function getCurrentUse() {
  return request('manager/battery_setting/current_use');
}
