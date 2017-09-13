import service from '../utils/axios';

export function getVirtualCard() {
  return service.get('virtual_card');
}

export function openVirtualCardService() {
  return service({
    method: 'PUT',
    url: 'user/virtual_card',
  });
}

// 充值押金
export function payDeposit() {
  return service({
    method: 'POST',
    url: 'virtual_card/deposit',
    data: {},
  });
}

// 充值
export function ercharge(money) {
  return service({
    method: 'POST',
    url: 'virtual_card/balance/top_up',
    data: {
      top_up_fee: money,
      openid: localStorage.getItem('openid'),
    },
  });
}

// 消费记录
export function record() {
  const id = localStorage.token;
  return service.get(`virtual_card/consume_record?username=${id}`);
}

// 租用电池
export function rentBattery(number) {
  return service({
    method: 'POST',
    url: 'battery_rent/rent',
    data: {
      serial_number: number,
    },
  });
}

// 进行保修
export function batteryReport(number) {
  return service({
    method: 'PUT',
    url: 'battery_rent/battery_report',
    data: {
      serial_number: number,
    },
  });
}

// 正在使用的电池
export function inuseBattery() {
  return service.get('battery_rent/battery');
}
