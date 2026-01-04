import Vue from 'vue'
import VueRouter from 'vue-router'
import HomePage from '../components/Home.vue'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import PasswordRecovery from '../components/PasswordRecovery.vue'
import Products from '../components/Products.vue'
import Offers from '../components/Offers.vue'
import ProductDetails from '../components/ProductDetails.vue'
import Cart from '../components/Cart.vue'
import Checkout from '../components/Checkout.vue'
import Receipt from '../components/Receipt.vue'
import Favorites from '../components/Favorites.vue' // Importar el nuevo componente Favorites

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/registro',
    name: 'Register',
    component: Register
  },
  {
    path: '/recuperar-contraseña',
    name: 'PasswordRecovery',
    component: PasswordRecovery
  },
  {
    path: '/productos',
    name: 'Products',
    component: Products
  },
  {
    path: '/ofertas',
    name: 'Offers',
    component: Offers
  },
  {
    path: '/producto/:id',
    name: 'ProductDetails',
    component: ProductDetails,
    props: true
  },
  {
    path: '/carrito',
    name: 'Cart',
    component: Cart
  },
  {
    path: '/checkout',
    name: 'Checkout',
    component: Checkout
  },
  {
    path: '/factura',
    name: 'Receipt',
    component: Receipt
  },
  {
    path: '/favoritos',
    name: 'Favorites',
    component: Favorites
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
