export const order = {
  id: '订单号',
  appointment_fee: '已支付预约金',
  appointment_fee_needed: '需交预约金',
  category: '种类',
  color: '颜色',
  data: '时间',
  delivery: '配送方式',
  e_bike_model: '类型',
  expired_date_time: '订单过期时间',
  note: '留言',
  price: '价格',
  reduced_price: '优惠价格',
  rent_deposit: '已交押金',
  rent_deposit_needed: '需要押金',
  rent_time_period: '租用时间',
  serial_number: '车辆编号',
  type: '订单类型',
  user: '用户',
  status: '状态',
};
export const carConstant = {
  name: '名称',
  type: '类型',
  category: '类别',
  battery: '电池',
  configure: '配置',
  distance: '续航',
  // introduction: '商品简介',
  num_sold: '销量',
  num_view: '浏览量',
  price: '价格',

};

export const Const = {
  key: '名称',
  value: '值',
};

// 商铺
export const Store = {
  name: '名称',
  address: '地址',
};


export const School = {
  name: '名称',
  address: '地址',
  store: '所属商铺',
};


export const User = {
  username: '用户名',
  // password: '密码',
  name: '姓名',
  school: '学校',
  student_id: '学号',
  phone: '电话',
  identify_number: '身份证号',
  we_chat_id: '微信号',
  account: '退款账号',
  account_type: '账号类型',
  status: '租用状态',
  admin: '管理权限'
};


export const VirtualCard = {
  card_no: '卡号',
  deposit: '押金',
  balance: '余额',
  situation: '冻结状态',

};

export const ConsumeRecord = {
  card: '卡号',
  consume_event: '消费事件类型',
  consume_date_time: '消费日期',
  consume_fee: '消费金额',
  balance: '余额',

};


export const EBikeModel = {
  name: '名称',
  category: '类别',
  type: '类型',
  price: '价格',
  colors: '颜色',
  distance: '续航',
  configure: '配置',
  battery: '电池规格',
  image_urls: '轮播图',
  introduction_image_urls: '介绍图',
  introduction: '文字介绍',
  num_sold: '销售量',
  num_view: '浏览量',
};
// 库存
export const Storage = {
  model: '电动车型号',
  color: '颜色',
  num: '数量',
};

// 电池
export const Battery = {
  serial_number: '编号',
  desc: '描述',
  on_loan: '租用状态',
  user: '用户',
};

// 电池记录
export const BatteryRecord = {
  user: '用户',
  battery: '电池',
  rent_date: '租用日期',
  return_date: '归还日期',
  price: '租用价格',
  situation: '租用状态',

};
// 电池报修
export const BatteryReport = {
  battery: '电池',
  current_owner: '当前使用人',
  report_time: '报修时间',
};

export const CouponTemplate = {
  id: "模板编号",
  desc: '描述',
  situation: '使用条件',
  value: '减免价格',
  duration: '有效周期',
};


export const Coupon = {
  desc: '描述',
  user: '用户',
  situation: '使用条件',
  value: '减免价格',
  expired: '到期日期',
  status: '状态',
  template_no: '优惠劵模板编号',
};

// 编号
export const SerialNumber = {
  code: '编号',
  store: '所有商铺',
  store_code: '商铺编号',
  category_code: '类别编号',
  available: '有效状态',
  appointment: '订单号',
  battery: '电池',
};
// 退款
export const RefundTable = {
  id: '编号',
  user: '用户',
  out_trade_no: "商户付款订单号",
  type: '退款类型',
  value: '退款金额',
  date: '日期',
  comment: '备注',
  status: '状态',
  // account: '退款账号',
  // account_type: '账号类型',
};
// 电动车报修
export const ReportTable = {
  appointment: '订单号',
  user: '用户',
  address: '地址',
  comment: '备注',
  phone: '电话',
  date: '日期',
};
