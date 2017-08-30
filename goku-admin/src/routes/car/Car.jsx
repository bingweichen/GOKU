import React, { Component } from 'react';
import { Table, Button } from 'antd';
import { connect } from 'dva';
import CarModal from '../../components/Modal/CarModal';
import { carConstant } from '../../utils/constant.js';
import constructionDS from '../../utils/Table/constructionDS.js';

const columns = constructionDS(carConstant);
class Car extends Component {
  componentDidMount() {

  }

  render() {
    const {
      dataSource,
      loading,
      total,
      dispatch,
      toggleVisible,
      visible,
      setIsEdit,
      isEdit,
      record } = this.props;
    const cols = columns.concat([{
      title: '详情',
      dataIndex: 'detail',
      render: (text, records) => {
        return (
          <Button
            onClick={() => {
              this.props.setIsEdit(true);
              this.props.toggleVisible(true);
              this.props.dispatch({ type: 'car/setRecord', record: records });
            }}
          >
            编辑
      </Button >
        );
      },
    }]);
    return (
      <div>
        <Button
          type="primary"
          onClick={() => {
            setIsEdit(false);
            toggleVisible(true);
          }}
        >
          添加
      </Button>
        <CarModal
          visible={visible}
          toggleVisible={toggleVisible}
          isEdit={isEdit}
          record={record}
        />
        <Table
          dataSource={dataSource}
          columns={cols}
          loading={loading}
          pagination={{
            onChange: (page, pageSize) => {
              dispatch({
                page,
                type: 'car/getDataSource',
                number: pageSize,
              });
            },
            total,
          }}
        />
      </div>
    );
  }
}

const mapStateToProps = ({
  loading: { global },
  car: {
    dataSource,
    visible,
    isEdit,
    record,
  },
}) => {
  return {
    dataSource,
    visible,
    loading: global,
    total: 30,
    isEdit,
    record,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    dispatch,
    toggleVisible: visible => dispatch({ type: 'car/setVisible', visible }),
    setIsEdit: isEdit => dispatch({ type: 'car/setEditStatus', isEdit }),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(Car);
