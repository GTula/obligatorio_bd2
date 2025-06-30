export const validarCI = (ci) => {
  // Convertir a string y limpiar
  const ciStr = ci.toString().replace(/\D/g, '');
  
  // Debe tener exactamente 8 dígitos
  if (ciStr.length !== 8) {
    return false;
  }
  
  // Algoritmo de validación de cédula uruguaya
  const digits = ciStr.split('').map(Number);
  const checkDigit = digits[7];
  
  // Coeficientes para el cálculo
  const coefficients = [2, 9, 8, 7, 6, 3, 4];
  
  let sum = 0;
  for (let i = 0; i < 7; i++) {
    sum += digits[i] * coefficients[i];
  }
  
  const remainder = sum % 10;
  const calculatedCheckDigit = remainder === 0 ? 0 : 10 - remainder;
  
  return calculatedCheckDigit === checkDigit;
};

export const formatearCI = (ci) => {
  const ciStr = ci.toString().replace(/\D/g, '');
  if (ciStr.length === 8) {
    return `${ciStr.slice(0, 1)}.${ciStr.slice(1, 4)}.${ciStr.slice(4, 7)}-${ciStr.slice(7)}`;
  }
  return ci;
};
