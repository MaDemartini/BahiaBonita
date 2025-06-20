document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('form-reserva');
  const errorDiv = document.getElementById('error-capacidad');

  const nombreInput = document.getElementById('nombre');
  const apellidoInput = document.getElementById('apellido');
  const ingresoInput = document.getElementById('fecha_ingreso');
  const salidaInput = document.getElementById('fecha_salida');
  const adultosInput = document.getElementById('cant_adultos');
  const ninosInput = document.getElementById('cant_ninos');

  const precioNoche = parseFloat(document.getElementById("reserva-precio-noche").dataset.valor);
  const capacidadMax = parseInt(document.getElementById("reserva-capacidad").dataset.valor);
  const departamentoId = parseInt(document.getElementById("reserva-id").dataset.valor);
  const csrfToken = document.querySelector("meta[name='csrf-token']").getAttribute("content");

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    const fecha_ingreso = ingresoInput.value;
    const fecha_salida = salidaInput.value;

    fetch("/reservas/validar/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken
      },
      body: JSON.stringify({
        fecha_ingreso,
        fecha_salida,
        departamento_id: departamentoId
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.disponible) {
        form.submit(); // aún podrías deshabilitar esto si solo quieres botón pago
      } else {
        errorDiv.style.display = "block";
        errorDiv.innerText = data.mensaje || "No disponible en esas fechas.";
      }
    })
    .catch(() => {
      errorDiv.style.display = "block";
      errorDiv.innerText = "Error al validar la reserva.";
    });
  });

  function actualizarComprobante() {
    const adultos = parseInt(adultosInput.value) || 0;
    const ninos = parseInt(ninosInput.value) || 0;
    const totalPersonas = adultos + ninos;

    const fi = new Date(ingresoInput.value);
    const fs = new Date(salidaInput.value);
    const dias = (fs - fi) / (1000 * 60 * 60 * 24);
    let total = 0;

    const btnPago = document.getElementById("btn-pago");
    const btnHTML = `
      <button class="btn btn-secondary w-100 mt-3" disabled>Completa el formulario para continuar al pago</button>
    `;

    if (totalPersonas > capacidadMax) {
      errorDiv.textContent = `La suma de adultos y niños no puede superar la capacidad máxima del departamento (${capacidadMax} personas).`;
      errorDiv.style.display = 'block';
      btnPago.innerHTML = btnHTML;
      return;
    } else if (totalPersonas === 0) {
      errorDiv.textContent = 'Debe ingresar al menos una persona.';
      errorDiv.style.display = 'block';
      btnPago.innerHTML = btnHTML;
      return; 
    } else if (adultos === 0){
      errorDiv.textContent = 'Debe ingresar al menos un adulto.';
      errorDiv.style.display = 'block';
      btnPago.innerHTML = btnHTML;
      return;    
    } else if (dias <= 0 || isNaN(dias)) {
      errorDiv.textContent = 'Las fechas ingresadas no son válidas. La fecha de salida debe ser posterior a la de ingreso.';
      errorDiv.style.display = 'block';
      btnPago.innerHTML = btnHTML;
      return;
    } else{
      // Si pasó todas las validaciones
      errorDiv.style.display = 'none';
      total = dias * precioNoche;
    }

    // Actualizar comprobante
    document.getElementById("comp_nombre_apellido").textContent = `${nombreInput?.value || 'Nombre'} ${apellidoInput?.value || 'Apellido'}`;
    document.getElementById("comp_fecha_ingreso").textContent = ingresoInput.value || '-';
    document.getElementById("comp_fecha_salida").textContent = salidaInput.value || '-';
    document.getElementById("comp_cant_adultos").textContent = adultos;
    document.getElementById("comp_cant_ninos").textContent = ninos;
    document.getElementById("comp_cant_total").textContent = totalPersonas;
    document.getElementById("comp_valor_total").textContent = total.toFixed(0);

    // Botón activo (formulario válido)
    btnPago.innerHTML = `
      <form method="POST" action="/transbank/inicio_pago/">
        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
        <input type="hidden" name="nombre" value="${nombreInput?.value}">
        <input type="hidden" name="apellido" value="${apellidoInput?.value}">
        <input type="hidden" name="fecha_ingreso" value="${ingresoInput.value}">
        <input type="hidden" name="fecha_salida" value="${salidaInput.value}">
        <input type="hidden" name="cant_adultos" value="${adultos}">
        <input type="hidden" name="cant_ninos" value="${ninos}">
        <input type="hidden" name="departamento_id" value="${departamentoId}">
        <button type="submit" class="btn btn-success w-100 mt-3">Ir al Pago</button>
      </form>
    `;
}

  // Escuchar cambios
  [nombreInput, apellidoInput, ingresoInput, salidaInput, adultosInput, ninosInput].forEach(el => {
    if (el) el.addEventListener('input', actualizarComprobante);
  });

  actualizarComprobante(); // Ejecutar al cargar
});
