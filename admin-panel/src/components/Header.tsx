import React from 'react';
import styled from 'styled-components';
import { Menu, Bell, User } from 'lucide-react';

const HeaderContainer = styled.header`
  background: #ffffff;
  border-bottom: 1px solid #e9ecef;
  padding: 16px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  z-index: 100;
`;

const LeftSection = styled.div`
  display: flex;
  align-items: center;
  gap: 16px;
`;

const MenuButton = styled.button`
  display: none;
  padding: 8px;
  border: none;
  background: transparent;
  cursor: pointer;
  color: #6c757d;
  
  @media (max-width: 768px) {
    display: flex;
    align-items: center;
    justify-content: center;
  }
`;

const PageTitle = styled.h1`
  font-size: 24px;
  font-weight: 600;
  color: #212529;
  margin: 0;
`;

const RightSection = styled.div`
  display: flex;
  align-items: center;
  gap: 16px;
`;

const NotificationButton = styled.button`
  padding: 8px;
  border: none;
  background: transparent;
  cursor: pointer;
  color: #6c757d;
  position: relative;
  
  &:hover {
    color: #007bff;
  }
`;

const NotificationBadge = styled.span`
  position: absolute;
  top: 4px;
  right: 4px;
  width: 8px;
  height: 8px;
  background: #dc3545;
  border-radius: 50%;
`;

const UserButton = styled.button`
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border: none;
  background: transparent;
  cursor: pointer;
  color: #6c757d;
  border-radius: 6px;
  
  &:hover {
    background: #f8f9fa;
    color: #007bff;
  }
`;

const UserInfo = styled.div`
  display: flex;
  flex-direction: column;
  align-items: flex-start;
`;

const UserName = styled.span`
  font-size: 14px;
  font-weight: 500;
  color: #212529;
`;

const UserRole = styled.span`
  font-size: 12px;
  color: #6c757d;
`;

interface HeaderProps {
  onMenuClick: () => void;
}

const Header: React.FC<HeaderProps> = ({ onMenuClick }) => {
  const getPageTitle = () => {
    const path = window.location.pathname;
    switch (path) {
      case '/dashboard': return 'Дашборд';
      case '/users': return 'Пользователи';
      case '/funds': return 'Фонды';
      case '/campaigns': return 'Кампании';
      case '/reports': return 'Отчеты';
      case '/settings': return 'Настройки';
      default: return 'Админ-панель';
    }
  };

  return (
    <HeaderContainer>
      <LeftSection>
        <MenuButton onClick={onMenuClick}>
          <Menu size={20} />
        </MenuButton>
        <PageTitle>{getPageTitle()}</PageTitle>
      </LeftSection>
      
      <RightSection>
        <NotificationButton>
          <Bell size={20} />
          <NotificationBadge />
        </NotificationButton>
        
        <UserButton>
          <User size={20} />
          <UserInfo>
            <UserName>Администратор</UserName>
            <UserRole>Super Admin</UserRole>
          </UserInfo>
        </UserButton>
      </RightSection>
    </HeaderContainer>
  );
};

export default Header;
