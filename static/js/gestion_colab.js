
// funcion para hacer el boton burger
document.addEventListener('DOMContentLoaded', () => {
  const menuToggle = document.getElementById('menuToggle');
  const sidebar = document.getElementById('sidebar');
  const mainContent = document.getElementById('main-content');

  // Botón para abrir/cerrar
  menuToggle.addEventListener('click', () => {
    sidebar.classList.toggle('show');
    mainContent.classList.toggle('shifted');
  });

  // Cerrar al hacer clic fuera
  document.addEventListener('click', (event) => {
    // Si no está abierto, no hacer nada
    if (!sidebar.classList.contains('show')) return;

    // Si clic en botón o sidebar, no cerrar
    if (sidebar.contains(event.target) || menuToggle.contains(event.target)) return;

    // Clic afuera -> cerrar
    sidebar.classList.remove('show');
    mainContent.classList.remove('shifted');
    
  });
  // sidebar.querySelectorAll('a').forEach(link => {
  //   link.addEventListener('click', () => {
  //     sidebar.classList.remove('show');
  //     mainContent.classList.remove('shifted');
  //   });
  // });
});