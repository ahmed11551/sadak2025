import React from 'react';
import styled from 'styled-components';
import { Users, Search, Filter, MoreVertical } from 'lucide-react';

const UsersContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
`;

const PageHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
`;

const PageTitle = styled.h2`
  font-size: 24px;
  font-weight: 600;
  color: #212529;
  margin: 0;
`;

const SearchBar = styled.div`
  display: flex;
  gap: 12px;
  align-items: center;
`;

const SearchInput = styled.input`
  padding: 10px 12px;
  border: 1px solid #ced4da;
  border-radius: 6px;
  font-size: 14px;
  width: 300px;
  
  &:focus {
    outline: none;
    border-color: #007bff;
  }
`;

const FilterButton = styled.button`
  padding: 10px 16px;
  border: 1px solid #ced4da;
  background: #ffffff;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  
  &:hover {
    background: #f8f9fa;
  }
`;

const UsersTable = styled.div`
  background: #ffffff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 1px solid #e9ecef;
`;

const TableHeader = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr 1fr auto;
  gap: 16px;
  padding: 16px 24px;
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
  font-weight: 600;
  font-size: 14px;
  color: #6c757d;
`;

const TableRow = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr 1fr auto;
  gap: 16px;
  padding: 16px 24px;
  border-bottom: 1px solid #f8f9fa;
  align-items: center;
  
  &:last-child {
    border-bottom: none;
  }
  
  &:hover {
    background: #f8f9fa;
  }
`;

const UserAvatar = styled.div`
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #007bff;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
`;

const UserInfo = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
`;

const UserDetails = styled.div`
  display: flex;
  flex-direction: column;
`;

const UserName = styled.div`
  font-weight: 500;
  color: #212529;
`;

const UserEmail = styled.div`
  font-size: 12px;
  color: #6c757d;
`;

const StatusBadge = styled.span<{ status: 'active' | 'inactive' | 'premium' }>`
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  
  ${props => {
    switch (props.status) {
      case 'active':
        return 'background: #d4edda; color: #155724;';
      case 'inactive':
        return 'background: #f8d7da; color: #721c24;';
      case 'premium':
        return 'background: #fff3cd; color: #856404;';
      default:
        return 'background: #e2e3e5; color: #383d41;';
    }
  }}
`;

const ActionButton = styled.button`
  padding: 8px;
  border: none;
  background: transparent;
  cursor: pointer;
  color: #6c757d;
  border-radius: 4px;
  
  &:hover {
    background: #f8f9fa;
    color: #007bff;
  }
`;

const EmptyState = styled.div`
  text-align: center;
  padding: 60px 20px;
  color: #6c757d;
`;

const EmptyIcon = styled.div`
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
  color: #6c757d;
`;

const UsersPage: React.FC = () => {
  // Mock данные
  const users = [
    {
      id: 1,
      name: 'Ахмед Ибрагимов',
      email: 'ahmed@example.com',
      telegramId: '@ahmed_ib',
      status: 'premium',
      joinDate: '2024-01-15',
      donations: 15
    },
    {
      id: 2,
      name: 'Фатима Алиева',
      email: 'fatima@example.com',
      telegramId: '@fatima_ali',
      status: 'active',
      joinDate: '2024-02-20',
      donations: 8
    },
    {
      id: 3,
      name: 'Мухаммад Хасан',
      email: 'muhammad@example.com',
      telegramId: '@muhammad_h',
      status: 'active',
      joinDate: '2024-03-10',
      donations: 23
    },
    {
      id: 4,
      name: 'Айша Нур',
      email: 'aysha@example.com',
      telegramId: '@aysha_nur',
      status: 'inactive',
      joinDate: '2024-01-05',
      donations: 3
    }
  ];

  const getStatusText = (status: string) => {
    switch (status) {
      case 'active': return 'Активен';
      case 'inactive': return 'Неактивен';
      case 'premium': return 'Premium';
      default: return 'Неизвестно';
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('ru-RU');
  };

  return (
    <UsersContainer>
      <PageHeader>
        <PageTitle>Пользователи</PageTitle>
        <SearchBar>
          <SearchInput 
            type="text" 
            placeholder="Поиск пользователей..." 
          />
          <FilterButton>
            <Filter size={16} />
            Фильтры
          </FilterButton>
        </SearchBar>
      </PageHeader>

      <UsersTable>
        <TableHeader>
          <div>Пользователь</div>
          <div>Telegram ID</div>
          <div>Статус</div>
          <div>Дата регистрации</div>
          <div>Пожертвований</div>
          <div></div>
        </TableHeader>
        
        {users.map((user) => (
          <TableRow key={user.id}>
            <div>
              <UserInfo>
                <UserAvatar>
                  {user.name.split(' ').map(n => n[0]).join('')}
                </UserAvatar>
                <UserDetails>
                  <UserName>{user.name}</UserName>
                  <UserEmail>{user.email}</UserEmail>
                </UserDetails>
              </UserInfo>
            </div>
            <div>{user.telegramId}</div>
            <div>
              <StatusBadge status={user.status as any}>
                {getStatusText(user.status)}
              </StatusBadge>
            </div>
            <div>{formatDate(user.joinDate)}</div>
            <div>{user.donations}</div>
            <div>
              <ActionButton>
                <MoreVertical size={16} />
              </ActionButton>
            </div>
          </TableRow>
        ))}
      </UsersTable>

      {users.length === 0 && (
        <EmptyState>
          <EmptyIcon>
            <Users size={32} />
          </EmptyIcon>
          <h3>Нет пользователей</h3>
          <p>Пользователи появятся здесь после регистрации</p>
        </EmptyState>
      )}
    </UsersContainer>
  );
};

export default UsersPage;
