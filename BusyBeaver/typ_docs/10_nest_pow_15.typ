#let power-tower(base, n) = {
  if n <= 1 {
    $#base$
  } else {
    $#base^(#power-tower(base, n - 1))$
  }
}

#for i in range(1, 16) {
  [#block[#box[$ #power-tower(10, i) $]] #label("pt" + str(i))]
}