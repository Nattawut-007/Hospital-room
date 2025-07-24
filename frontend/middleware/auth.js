export default defineNuxtRouteMiddleware(() => {
  const token = localStorage.getItem('token')
  if (!token) {
    return navigateTo('/login')
  }
})