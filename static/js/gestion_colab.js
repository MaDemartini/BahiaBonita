document.addEventListener('DOMContentLoaded', () => {
  const sidebar = document.getElementById('sidebar');
  const mainContent = document.getElementById('main-content');
  const agregarLink = document.getElementById('link-agregar-colaboradores');

  // -------------------------------
  // FUNCIÓN: Configurar botón hamburguesa
  // -------------------------------
  function engancharMenuToggle() {
    const menuToggle = document.getElementById('menuToggle');
    if (!menuToggle) return;

    menuToggle.addEventListener('click', (e) => {
      e.stopPropagation();
      sidebar.classList.toggle('show');
      mainContent.classList.toggle('shifted');
    });
  }

  // -------------------------------
  // Configurar botón hamburguesa inicial
  // -------------------------------
  engancharMenuToggle();

  // -------------------------------
  // Cerrar sidebar al hacer clic fuera
  // -------------------------------
  document.addEventListener('click', (event) => {
    if (!sidebar.classList.contains('show')) return;

    // Si clic dentro del sidebar o del menuToggle → no cerrar
    if (sidebar.contains(event.target) || event.target.closest('#menuToggle')) return;

    sidebar.classList.remove('show');
    mainContent.classList.remove('shifted');
  });

  // -------------------------------
  // Manejar click en "Agregar colaboradores"
  // -------------------------------
  agregarLink.addEventListener('click', function (e) {
    e.preventDefault();

    fetch('/administracion/agregar-colaborador-form/')
      .then(response => response.text())
      .then(html => {
        // Reemplaza el contenido
        mainContent.innerHTML = `
          <div id="menuToggle" class="menu-btn">
            <span></span><span></span><span></span>
          </div>
          ${html}
        `;

        // Cierra el sidebar
        sidebar.classList.remove('show');
        mainContent.classList.remove('shifted');

        //Engancha nuevamente el nuevo botón hamburguesa
        engancharMenuToggle();
      })
      .catch(err => {
        console.error('Error al cargar el formulario:', err);
        mainContent.innerHTML = '<p>Error al cargar el formulario. Intenta nuevamente.</p>';
      });
  });
});