import { createContext, useContext, useEffect, useRef, useState } from 'react';                                                                                         
  import { useAuth } from '@clerk/clerk-react';                                                                                                                           
  import { useLabourSession } from '@base/contexts';                                                                                                                      
                                                                                                                                                                          
  interface WebSocketContextValue {                                                                                                                                       
    isConnected: boolean;                                                                                                                                                 
    sendCommand: (payload: any) => void;                                                                                                                                  
    subscribe: (callback: (message: any) => void) => () => void;                                                                                                          
  }                                                                                                                                                                       
                                                                                                                                                                          
  const WebSocketContext = createContext<WebSocketContextValue | null>(null);                                                                                             
                                                                                                                                                                          
  export function WebSocketProvider({ children }: { children: React.ReactNode }) {                                                                                        
    const { getToken } = useAuth();                                                                                                                                       
    const { labourId } = useLabourSession();                                                                                                                              
    const [isConnected, setIsConnected] = useState(false);                                                                                                                
                                                                                                                                                                          
    const wsRef = useRef<WebSocket | null>(null);                                                                                                                         
    const subscribersRef = useRef<Set<(message: any) => void>>(new Set());                                                                                                
    const reconnectTimeoutRef = useRef<NodeJS.Timeout>();                                                                                                                 
                                                                                                                                                                          
    useEffect(() => {                                                                                                                                                     
      if (!labourId) {
        return
      };                                                                                                                                              
                                                                                                                                                                          
      const connect = async () => {                                                                                                                                       
        try {                                                                                                                                                             
          const token = await getToken();                                                                                                                                 
          const wsUrl = import.meta.env.VITE_LABOUR_SERVICE_WEBSOCKET || '';                                                                                              
                                                                                                                                                                          
          const ws = new WebSocket(                                                                                                                                       
            `${wsUrl}${labourId}`,                                                                                                                                        
            `base64url.bearer.authorization.fernlabour.com.${token}`                                                                                                      
          );                                                                                                                                                              
                                                                                                                                                                          
          ws.onopen = () => {                                                                                                                                             
            console.log('[WebSocket] Connected');                                                                                                                         
            setIsConnected(true);                                                                                                                                         
            wsRef.current = ws;                                                                                                                                           
          };                                                                                                                                                              
                                                                                                                                                                          
          ws.onmessage = (event) => {                                                                                                                                     
            const message = JSON.parse(event.data);                                                                                                                       
                                                                                                                                                                                                                                                                                 
            subscribersRef.current.forEach(callback => callback(message));                                                                                                
          };                                                                                                                                                              
                                                                                                                                                                          
          ws.onerror = (error) => {                                                                                                                                       
            console.error('[WebSocket] Error:', error);                                                                                                                   
          };                                                                                                                                                              
                                                                                                                                                                          
          ws.onclose = () => {                                                                                                                                            
            console.log('[WebSocket] Disconnected');                                                                                                                      
            setIsConnected(false);                                                                                                                                        
            wsRef.current = null;                                                                                                                                         
                                                                                                                                                                                                                                                                                       
            reconnectTimeoutRef.current = setTimeout(connect, 3000);                                                                                                      
          };                                                                                                                                                              
        } catch (error) {                                                                                                                                                 
          console.error('[WebSocket] Connection failed:', error);                                                                                                         
          reconnectTimeoutRef.current = setTimeout(connect, 3000);                                                                                                        
        }                                                                                                                                                                 
      };                                                                                                                                                                  
                                                                                                                                                                          
      connect();                                                                                                                                                          
                                                                                                                                                                          
      return () => {                                                                                                                                                      
        clearTimeout(reconnectTimeoutRef.current);                                                                                                                        
        wsRef.current?.close();                                                                                                                                           
      };                                                                                                                                                                  
    }, [labourId, getToken]);                                                                                                                                             
                                                                                                                                                                          
    const sendCommand = (payload: any) => {                                                                                                                               
      if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {                                                                                                 
        wsRef.current.send(JSON.stringify(payload));                                                                                                                      
      } else {                                                                                                                                                                                                                                                            
        throw new Error('WebSocket not connected');                                                                                                                       
      }                                                                                                                                                                   
    };                                                                                                                                                                    
                                                                                                                                                                          
    const subscribe = (callback: (message: any) => void) => {                                                                                                             
      subscribersRef.current.add(callback);                                                                                                                               
      return () => {                                                                                                                                                      
        subscribersRef.current.delete(callback);                                                                                                                          
      };                                                                                                                                                                  
    };                                                                                                                                                                    
                                                                                                                                                                          
    return (                                                                                                                                                              
      <WebSocketContext.Provider value={{ isConnected, sendCommand, subscribe }}>                                                                                         
        {children}                                                                                                                                                        
      </WebSocketContext.Provider>                                                                                                                                        
    );                                                                                                                                                                    
  }                                                                                                                                                                       
                                                                                                                                                                          
  export function useWebSocket() {                                                                                                                                        
    const context = useContext(WebSocketContext);                                                                                                                         
    if (!context) {                                                                                                                                                       
      throw new Error('useWebSocket must be used within WebSocketProvider');                                                                                              
    }                                                                                                                                                                     
    return context;                                                                                                                                                       
  }               