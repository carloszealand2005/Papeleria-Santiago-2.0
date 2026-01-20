import Vue from 'vue'
import VueRouter from 'vue-router'
import HomePage from '../components/Home.vue'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import RegisterWholesale from '../components/RegisterWholesale.vue'
import PasswordRecovery from '../components/PasswordRecovery.vue'
import Products from '../components/Products.vue'
import ProductsSearch from '../components/ProductsSearch.vue'
import Offers from '../components/Offers.vue'
import ProductDetails from '../components/ProductDetails.vue'
import Cart from '../components/Cart.vue'
import Checkout from '../components/Checkout.vue'
import Receipt from '../components/Receipt.vue'
import Favorites from '../components/Favorites.vue' // Importar el nuevo componente Favorites
import MyAccount from '../components/MyAccount.vue'
import VerificationCode from '../components/VerificationCode.vue'

Vue.use(VueRouter)

// Evitar warnings/errores por navegación redundante (Vue Router 3)
// Solo ignoramos NavigationDuplicated; otros errores siguen siendo visibles.
const isNavigationDuplicated = (err) => {
  return (
    err &&
    (err.name === 'NavigationDuplicated' ||
      err._name === 'NavigationDuplicated' ||
      (typeof err.message === 'string' && err.message.includes('Avoided redundant navigation')))
  );
};

const originalPush = VueRouter.prototype.push;
VueRouter.prototype.push = function push(location, onResolve, onReject) {
  // Soporta firma callback y Promise
  if (onResolve || onReject) return originalPush.call(this, location, onResolve, onReject);
  return originalPush.call(this, location).catch((err) => {
    if (isNavigationDuplicated(err)) return this.currentRoute;
    return Promise.reject(err);
  });
};

const originalReplace = VueRouter.prototype.replace;
VueRouter.prototype.replace = function replace(location, onResolve, onReject) {
  if (onResolve || onReject) return originalReplace.call(this, location, onResolve, onReject);
  return originalReplace.call(this, location).catch((err) => {
    if (isNavigationDuplicated(err)) return this.currentRoute;
    return Promise.reject(err);
  });
};

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
    path: '/registro/mayorista',
    name: 'RegisterWholesale',
    component: RegisterWholesale
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
    path: '/productos/search',
    name: 'ProductsSearch',
    component: ProductsSearch
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
  },
  {
    path: '/mi-cuenta',
    name: 'MyAccount',
    component: MyAccount
  },
  {
    path: '/verificacion',
    name: 'VerificationCode',
    component: VerificationCode
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
