let result = 0;
const index = [0, -0.927, 24.59, -46.7, -11.75, 86.67, -38.1, -36.8, 24];
//const index = [0, 1]
for(let i = 0; i < index.length; i++){
  result += index[i]*Math.pow(10, i);
}
console.log(result);
