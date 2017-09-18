import constructionDS from './constructionDS';
import * as constant from '../constant';

export const schoolCol = constructionDS(constant.School);
export const couponCol = constructionDS(constant.CouponTemplate);
export const storageCol = constructionDS(constant.Storage);
export const batteryCol = constructionDS(constant.Battery);
export const batteryRecord = constructionDS(constant.BatteryRecord);
export const batteryReport = constructionDS(constant.BatteryReport);
export const serialNumber = constructionDS(constant.SerialNumber);
export const refundCol = constructionDS(constant.RefundTable);
export const reportCol = constructionDS(constant.ReportTable);
export const storeCol = constructionDS(constant.Store);
export const UserCouponCol = constructionDS(constant.Coupon);
export const VirtualCardCol = constructionDS(constant.VirtualCard);
