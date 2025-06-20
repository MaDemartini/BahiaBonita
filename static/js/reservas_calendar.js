document.addEventListener('DOMContentLoaded', () => {
    const ingresoInput = document.getElementById('fecha_ingreso');
    const salidaInput = document.getElementById('fecha_salida');
    const errorDiv = document.getElementById('error_fechas');
    const departamentoId = ingresoInput?.dataset.departamento;
    if (!ingresoInput || !salidaInput || typeof departamentoId === 'undefined') return;

    let reservas = [];

    fetch(`/reservas/${departamentoId}/fechas/`)
        .then(r => r.json())
        .then(data => {
            reservas = data.fechas || [];

            const disabledRanges = reservas.map(r => ({ from: r.desde, to: r.hasta }));

            const opts = {
                dateFormat: 'Y-m-d',
                minDate: 'today',
                disable: disabledRanges,
                onChange: validarTraslape
            };

            flatpickr(ingresoInput, opts);
            flatpickr(salidaInput, opts);
        });

    function validarTraslape() {
        if (!ingresoInput.value || !salidaInput.value) return;

        const ingreso = ingresoInput.value;
        const salida = salidaInput.value;

        errorDiv.textContent = "";

        for (const r of reservas) {
            if (r.desde <= salida && ingreso <= r.hasta) {
                errorDiv.textContent = `Este departamento esta reservado desde el ${r.desde} al ${r.hasta} intenta con otra fecha.`;
                break;
            }
        }
    }



});



