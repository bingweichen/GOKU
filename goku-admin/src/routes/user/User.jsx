import React, { Component } from 'react';
import { Table } from 'antd';
import { connect } from 'dva';
import { User as UserConstant } from '../../utils/constant.js';
import constructionDS from '../../utils/Table/constructionDS.js';

const columns = constructionDS(UserConstant);

class User extends Component {
  render() {
    const { dataSource, loading } = this.props;
    return (
      <div>
        <Table
          columns={columns}
          dataSource={dataSource}
          loading={loading}
        />
      </div>
    );
  }
}

const mapStateToProps = ({ user, loading: { global } }) => {
  return {
    dataSource: user.dataSource,
    loading: global,
  };
};

export default connect(mapStateToProps)(User);
