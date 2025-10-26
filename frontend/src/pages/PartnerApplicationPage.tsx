import React from 'react';
import styled from 'styled-components';
import { FileText, ArrowLeft } from 'lucide-react';
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
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
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

const PartnerApplicationPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <PageContainer>
      <Header>
        <BackButton onClick={() => navigate('/')}>
          <ArrowLeft size={24} />
        </BackButton>
        <Title>Партнерство</Title>
      </Header>
      
      <Content>
        <Icon>
          <FileText size={40} />
        </Icon>
        <Message>Страница партнерства в разработке</Message>
        <SubMessage>Здесь будет форма для подачи заявки на партнерство</SubMessage>
      </Content>
    </PageContainer>
  );
};

export default PartnerApplicationPage;
