// PIERWSZE ROZWIAZANIE
// Definicje zmiennych - musisz dostarczyć odpowiednie wartości
let brutto = ...;  // I2
let rata_k = ...;  // I3
let q = ...;       // I1
let okres = ...;   // B11
let D1 = ...;      // D1 - musisz zdefiniować warunek, który będzie sprawdzany

let wynik;

if (D1 === "t") {
    wynik = (brutto - (rata_k * ((1 - Math.pow(q, okres)) / (1 - q)))) * #ADR!;
} else {
    wynik = brutto - (rata_k * ((1 - Math.pow(q, okres)) / (1 - q)));
}

// Wyświetl wynik
console.log(wynik);


// Drugie rozwiazanie
// Zakładając, że zmienne brutto, rata_k, q, okres oraz flaga są wcześniej zdefiniowane.
// Trzeba ustalić co to jest #ADR! w twoim kontekście i odpowiednio dostosować.

const obliczRate = (brutto, rata_k, q, okres, flaga) => {
    const potega = Math.pow(q, okres);
    let wynik;
  
    if (flaga === "t") {
      // Jeśli #ADR! jest mnożnikiem, musisz ustalić jego wartość.
      // Na przykład:
      const ADR = 1; // Tylko przykładowa wartość, musisz ją dostosować.
      wynik = (brutto - (rata_k * ((1 - potega) / (1 - q)))) * ADR;
    } else {
      wynik = brutto - (rata_k * ((1 - potega) / (1 - q)));
    }
  
    return wynik;
  };
  
  // Użycie funkcji z przykładowymi wartościami
  const wynikRaty = obliczRate(brutto, rata_k, q, okres, 't');
  console.log(wynikRaty);
  