import React, { createContext, useContext, useState, useEffect } from 'react'
import { useQuery, useQueryClient } from 'react-query'
import toast from 'react-hot-toast'

import { User } from '../types'
import { authAPI } from '../services/api'

interface AuthContextType {
  user: User | null
  login: (email: string, password: string) => Promise<void>
  register: (userData: {
    email: string
    password: string
    full_name: string
    preferred_language: string
  }) => Promise<void>
  logout: () => void
  loading: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [loading, setLoading] = useState(true)
  const queryClient = useQueryClient()
  
  const { data: user, isLoading } = useQuery(
    'currentUser',
    authAPI.getCurrentUser,
    {
      enabled: !!localStorage.getItem('token'),
      retry: false,
      onError: () => {
        localStorage.removeItem('token')
      },
      onSettled: () => {
        setLoading(false)
      },
    }
  )

  useEffect(() => {
    if (!localStorage.getItem('token')) {
      setLoading(false)
    }
  }, [])

  const login = async (email: string, password: string) => {
    try {
      const response = await authAPI.login(email, password)
      localStorage.setItem('token', response.access_token)
      
      // Refetch user data
      await queryClient.invalidateQueries('currentUser')
      toast.success('Login successful!')
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Login failed')
      throw error
    }
  }

  const register = async (userData: {
    email: string
    password: string
    full_name: string
    preferred_language: string
  }) => {
    try {
      const response = await authAPI.register(userData)
      localStorage.setItem('token', response.access_token)
      
      // Refetch user data
      await queryClient.invalidateQueries('currentUser')
      toast.success('Registration successful!')
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Registration failed')
      throw error
    }
  }

  const logout = () => {
    localStorage.removeItem('token')
    queryClient.clear()
    toast.success('Logged out successfully')
  }

  return (
    <AuthContext.Provider
      value={{
        user: user || null,
        login,
        register,
        logout,
        loading: loading || isLoading,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}