
//Se necesita cuando haces peticiones con fetch() en el frontend y tienes que enviar el CSRF token en los headers.
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie string begins with the name we want
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
document.addEventListener('DOMContentLoaded', function () {
    const modalEditarDepto = document.getElementById('modalEditarDepto');

    // Cargar datos en el modal
    modalEditarDepto.addEventListener('show.bs.modal', function (event) {
        const btn = event.relatedTarget;
        document.getElementById('editar-id').value = btn.getAttribute('data-id');
        document.getElementById('editar-num').value = btn.getAttribute('data-num');
        document.getElementById('editar-dormitorios').value = btn.getAttribute('data-dormitorios');
        document.getElementById('editar-banos').value = btn.getAttribute('data-banos');
        document.getElementById('editar-piso').value = btn.getAttribute('data-piso');
        document.getElementById('editar-personas').value = btn.getAttribute('data-personas');
        document.getElementById('editar-valor').value = btn.getAttribute('data-valor');
        document.getElementById('editar-mant').checked = btn.getAttribute('data-mant') === 'True';
    });

    // Enviar PUT a la API
    const formEditar = document.getElementById('formEditar');
    formEditar.addEventListener('submit', function (e) {
        e.preventDefault();

        const id = document.getElementById('editar-id').value;
        const data = {
            num_depto: document.getElementById('editar-num').value,
            cant_dormitorios: document.getElementById('editar-dormitorios').value,
            cant_banos: document.getElementById('editar-banos').value,
            piso: document.getElementById('editar-piso').value,
            cant_personas: document.getElementById('editar-personas').value,
            valor_dia: document.getElementById('editar-valor').value,
            mantenimiento: document.getElementById('editar-mant').checked
        };

        console.log("Enviando PUT a /api/depto/" + id + "/", data);

        fetch(`/api/depto/${id}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
                
            },
            body: JSON.stringify(data)
        })
        .then(response => {
        console.log("Código de respuesta:", response.status);
        if (response.ok) {
            alert("Departamento actualizado correctamente");
            location.reload();
        } else {
            return response.json().then(err => {
                console.error("Error desde la API:", err);
                alert("Error al actualizar: " + JSON.stringify(err));
            });
        }
    })
    .catch(error => {
        console.error("Error en fetch:", error);
        alert("Error en la solicitud: " + error);
    });
    });
});

// Eliminar departamento
document.addEventListener('DOMContentLoaded', function () {
    const botonesEliminar = document.querySelectorAll('.btn-eliminar');

    botonesEliminar.forEach(boton => {
        boton.addEventListener('click', function () {
            const id = this.getAttribute('data-id');

            Swal.fire({
                title: '¿Estás seguro?',
                text: '¿Seguro deseas eliminar este departamento de forma permanente?',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#d33',
                cancelButtonColor: '#6c757d',
                confirmButtonText: 'Sí, eliminar',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.isConfirmed) {
                    // Enviar DELETE a la API
                    fetch(`/api/depto/${id}/`, {
                        method: 'DELETE',
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken')
                        }
                    })
                    .then(response => {
                        if (response.status === 204) {
                            Swal.fire({
                                icon: 'success',
                                title: '¡Eliminado!',
                                text: 'El departamento ha sido eliminado.',
                                timer: 1500,
                                showConfirmButton: false
                            }).then(() => {
                                location.reload();
                            });
                        } else {
                            return response.text().then(error => {
                                Swal.fire('Error', 'No se pudo eliminar el departamento.', 'error');
                                console.error('Error API:', error);
                            });
                        }
                    })
                    .catch(error => {
                        Swal.fire('Error', 'Error en la solicitud.', 'error');
                        console.error('Error en fetch:', error);
                    });
                }
            });
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.calendario-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            var deptoId = btn.getAttribute('data-depto');
            var input = document.getElementById('calendario-' + deptoId);
            input.style.display = 'block';

            // Obtener fechas reservadas para este departamento
            var fechas = (window.fechasReservadas[deptoId] || []).map(function(r) {
                var start = new Date(r.desde);
                var end = new Date(r.hasta);
                var dates = [];
                for (var d = new Date(start); d <= end; d.setDate(d.getDate() + 1)) {
                    dates.push(new Date(d).toISOString().slice(0,10));
                }
                return dates;
            }).flat();

            // Inicializar Flatpickr solo una vez
            if (!input._flatpickr) {
                flatpickr(input, {                
                    disable: fechas
                    
                });
            }
            // Mostrar el calendario
            input._flatpickr.open();
        });
    });
});
