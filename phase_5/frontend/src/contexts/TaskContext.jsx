import React, { createContext, useContext, useState } from 'react';

const TaskContext = createContext();

export const useTask = () => {
  const context = useContext(TaskContext);
  if (!context) {
    throw new Error('useTask must be used within a TaskProvider');
  }
  return context;
};

export const TaskProvider = ({ children }) => {
  const [taskUpdateTrigger, setTaskUpdateTrigger] = useState(0);

  const triggerTaskUpdate = () => {
    setTaskUpdateTrigger(prev => prev + 1);
  };

  const value = {
    taskUpdateTrigger,
    triggerTaskUpdate
  };

  return (
    <TaskContext.Provider value={value}>
      {children}
    </TaskContext.Provider>
  );
};