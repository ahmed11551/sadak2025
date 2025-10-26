import React from 'react';
import styled from 'styled-components';
import { DollarSign, ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const PageContainer = styled.div`
  padding: 20px 16px;
`;

const Header = styled.div`
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
`;

const BackButton = styled.button`
  background: none;
  border: none;
  padding: 8px;
  cursor: pointer;
  color: var(--tg-text-color, #000000);
`;

const Title = styled.h1`
  font-size: 24px;
  font-weight: 700;
  color: var(--tg-text-color, #000000);
`;

const Content = styled.div`
  text-align: center;
  padding: 40px 20px;
`;

const Icon = styled.div`
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 24px;
  color: white;
`;

const Message = styled.p`
  font-size: 18px;
  color: #6c757d;
  margin-bottom: 16px;
`;

const SubMessage = styled.p`
  font-size: 14px;
  color: #6c757d;
`;

const DonationPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <PageContainer>
      <Header>
        <BackButton onClick={() => navigate('/funds')}>
          <ArrowLeft size={24} />
        </BackButton>
        <Title>Пожертвование</Title>
      </Header>
      
      <Content>
        <Icon>
          <DollarSign size={40} />
        </Icon>
        <Message>Страница пожертвования в разработке</Message>
        <SubMessage>Здесь будет форма для разового пожертвования</SubMessage>
      </Content>
    </PageContainer>
  );
};

export default DonationPage;
