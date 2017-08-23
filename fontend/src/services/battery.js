import axios from 'axios';
import service from '../utils/axios';

export function getVirtualCard() {
  const id = localStorage.token;
  return service.get(`virtual_card?username=${id}`);
}

export function openVirtualCardService() {
  const id = localStorage.token;
  return axios({
    method: 'PUT',
    url: '/api/user/virtual_card',
    data: {
      card_no: id,
    },
  });
}

// 充值押金
export function payDeposit(money) {
  return axios({
    method: 'POST',
    url: '/api/virtual_card/deposit',
    data: {
      card_no: localStorage.token,
      deposit_fee: money,
    },
  });
}

// 充值
export function ercharge(money) {
  const id = localStorage.token;
  return service({
    method: 'POST',
    url: 'virtual_card/balance/top_up',
    data: {
      username: id,
      top_up_fee: money,
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
  const id = localStorage.token;
  return service({
    method: 'POST',
    url: 'battery_rent/rent',
    data: {
      username: id,
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
  const id = localStorage.token;
  return service.get(`battery_rent/battery?username=${id}`);
}
