import React, { Component } from 'react';
import { Table } from 'antd';
import PropTypes from 'prop-types';
import request from '../request.js';

class SimpleTable extends Component {

  state = {
    dataSource: [],
  }

  componentDidMount() {

  }

  render() {
    const { columns } = this.props;
    return (
      <div>
        <Table
          columns={columns}
          dataSource={this.state.dataSource}
        />
      </div>
    );
  }
};

SimpleTable.PropTypes = {
  url: PropTypes.string.isRequired,
};

export default SimpleTable;

