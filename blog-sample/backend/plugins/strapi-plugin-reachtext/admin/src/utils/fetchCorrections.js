const axios = require('axios');

const removeMd = require('remove-markdown');

export const fetchTextCorrections = (text) => {
  return axios.post('http://192.168.103.36:5000/text-correcting', { text: cleanText(text) })
}

export const cleanText = (text) => {
  const plainText = removeMd(text);
  return plainText;
}