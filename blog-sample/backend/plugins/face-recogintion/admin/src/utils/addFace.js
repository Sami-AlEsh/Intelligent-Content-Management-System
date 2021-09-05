const axios = require('axios');

export const addNewFace = (data) => {
  const formData = new FormData();
  formData.append("file", data.file, data.file.name);
  return axios.post('http://192.168.103.36:5000/add-face', formData, {
    params: { name: data.name }
  });
}