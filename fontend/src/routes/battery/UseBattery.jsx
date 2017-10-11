// 扫描之后进入的闪充页面
import React, { Component } from 'react';
import { Modal, Toast } from 'antd-mobile';
import { hashHistory } from 'dva/router';
import { rentBattery } from '../../services/battery.js';
import Button from '../../components/Button';
import styles from './index.less';

class UseBattery extends Component {

  state = {
    errorModal: false,
    errorMessage: '你现在暂时不能使用闪充',
  }

  async useBattery(number) {
    try {
      await rentBattery(number);
      Toast.success('租用电池成功', 1, () => hashHistory.replace('/?tab=flash'));
    } catch (error) {
      this.setState({ errorModal: true, errorMessage: error.message.message });
    }
  }

  render() {
    const { number } = this.props.location.query;
    return (
      <div className={styles.usebattery}>
        <div className={styles.batterInfo}>
          <p><span>闪充编号</span></p>
          <p>{number}</p>
        </div>
        <div className={styles.useMessage}>
          <Button
            style={{ width: '100%' }}
            onClick={() => { this.useBattery(number); }}
          >确认使用</Button>
          {/* <p>未交押金，无法享受闪充服务
          <span style={{ color: '#FF5B55' }}> 去充值</span>
          </p> */}
        </div>
        <Modal
          title="使用闪充失败"
          transparent
          maskClosable={false}
          visible={this.state.errorModal}
          footer={[{ text: '确定', onPress: () => { this.setState({ errorModal: false }); } }]}
        >
          {this.state.errorMessage}
        </Modal>
      </div>
    );
  }
}

export default UseBattery;
