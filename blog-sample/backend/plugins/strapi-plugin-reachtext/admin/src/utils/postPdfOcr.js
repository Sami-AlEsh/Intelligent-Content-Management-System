const axios = require('axios');

export const postPdfOCR = (file) => {
  const formData = new FormData();
  formData.append("file", file, file.name);
  return axios.post('http://192.168.103.36:5000/pdf-ocr', formData);
}
