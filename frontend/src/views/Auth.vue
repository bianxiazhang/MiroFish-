<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="logo-section">
          <img src="@/assets/logo.png" alt="渔知 Logo" class="logo" />
          <h1 class="brand-name">渔知</h1>
          <p class="brand-tagline">提取与创造，群体智能之海</p>
        </div>

      <div class="toggle-buttons">
        <button 
          class="toggle-btn" 
          :class="{ active: isLogin }"
          @click="isLogin = true"
        >
          登录
        </button>
        <button 
          class="toggle-btn" 
          :class="{ active: !isLogin }"
          @click="isLogin = false"
        >
          注册
        </button>
      </div>

      <form @submit.prevent="handleSubmit" class="auth-form">
        <div class="form-group">
          <label for="username">用户名</label>
          <input
            id="username"
            v-model="formData.username"
            type="text"
            placeholder="请输入用户名"
            required
            :disabled="loading"
          />
        </div>

        <div class="form-group">
          <label for="password">密码</label>
          <input
            id="password"
            v-model="formData.password"
            type="password"
            :placeholder="isLogin ? '请输入密码' : '密码至少6个字符'"
            required
            :disabled="loading"
          />
        </div>

        <div v-if="!isLogin" class="form-group">
          <label for="confirmPassword">确认密码</label>
          <input
            id="confirmPassword"
            v-model="formData.confirmPassword"
            type="password"
            placeholder="请再次输入密码"
            required
            :disabled="loading"
          />
        </div>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <button type="submit" class="submit-btn" :disabled="loading">
          {{ loading ? '处理中...' : (isLogin ? '登录' : '注册') }}
        </button>
      </form>

      <div class="auth-footer">
        <p>{{ isLogin ? '还没有账号？' : '已有账号？' }}</p>
        <a @click="isLogin = !isLogin" class="switch-link">
          {{ isLogin ? '立即注册' : '立即登录' }}
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import service from '../api/index.js'

const router = useRouter()

const isLogin = ref(true)
const loading = ref(false)
const error = ref('')

const formData = ref({
  username: '',
  password: '',
  confirmPassword: ''
})

const handleSubmit = async () => {
  error.value = ''
  
  if (!isLogin.value && formData.value.password !== formData.value.confirmPassword) {
    error.value = '两次输入的密码不一致'
    return
  }
  
  if (!isLogin.value && formData.value.password.length < 6) {
    error.value = '密码长度不能少于6个字符'
    return
  }
  
  loading.value = true
  
  try {
    const endpoint = isLogin.value ? '/api/auth/login' : '/api/auth/register'
    const response = await service.post(endpoint, {
      username: formData.value.username,
      password: formData.value.password
    })
    
    if (response.access_token) {
      localStorage.setItem('token', response.access_token)
      localStorage.setItem('user', JSON.stringify(response.user))
      router.push('/')
    } else if (!isLogin.value) {
      // 注册成功后自动登录
      const loginResponse = await service.post('/api/auth/login', {
        username: formData.value.username,
        password: formData.value.password
      })
      
      if (loginResponse.access_token) {
        localStorage.setItem('token', loginResponse.access_token)
        localStorage.setItem('user', JSON.stringify(loginResponse.user))
        router.push('/')
      }
    }
  } catch (err) {
    error.value = err.message || '操作失败，请稍后重试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.auth-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  padding: 40px;
  width: 100%;
  max-width: 420px;
}

.logo-section {
  text-align: center;
  margin-bottom: 30px;
}

.logo {
  width: 120px;
  height: auto;
  margin-bottom: 15px;
}

.brand-name {
  font-size: 2rem;
  font-weight: 700;
  color: #000;
  margin: 0 0 8px 0;
  letter-spacing: 2px;
}

.brand-tagline {
  color: #666;
  font-size: 0.9rem;
  margin: 0;
}

.toggle-buttons {
  display: flex;
  background: #f5f5f5;
  border-radius: 10px;
  padding: 4px;
  margin-bottom: 30px;
}

.toggle-btn {
  flex: 1;
  padding: 12px;
  border: none;
  background: transparent;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.3s ease;
  color: #666;
}

.toggle-btn.active {
  background: white;
  color: #000;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 0.9rem;
  font-weight: 500;
  color: #333;
}

.form-group input {
  padding: 14px 16px;
  border: 2px solid #e5e5e5;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s ease;
  outline: none;
}

.form-group input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-group input:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
}

.error-message {
  background: #fee;
  color: #c33;
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 0.9rem;
  text-align: center;
}

.submit-btn {
  padding: 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 10px;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.submit-btn:active:not(:disabled) {
  transform: translateY(0);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.auth-footer {
  text-align: center;
  margin-top: 25px;
  padding-top: 25px;
  border-top: 1px solid #e5e5e5;
}

.auth-footer p {
  color: #666;
  font-size: 0.9rem;
  margin: 0 0 8px 0;
}

.switch-link {
  color: #667eea;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  transition: color 0.3s ease;
}

.switch-link:hover {
  color: #764ba2;
}
</style>
