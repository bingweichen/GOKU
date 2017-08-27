// 根据 obj 构造dataSource
export default function constructionDS(obj) {
  return Object.keys(obj).map((key) => {
    return {
      key,
      title: obj[key],
      dataIndex: key,
    };
  });
}

