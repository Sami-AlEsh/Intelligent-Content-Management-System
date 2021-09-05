const axios = require('axios');

const removeMd = require('remove-markdown');

export const fetchAutoTags = (text) => {
  return axios.post('http://192.168.103.36:5000/auto-tagging', { text: cleanText(text), method: 'bert_cs' })
}

export const cleanText = (text) => {
  const plainText = removeMd(text);
  // console.log({ plainText });
  return plainText;
}