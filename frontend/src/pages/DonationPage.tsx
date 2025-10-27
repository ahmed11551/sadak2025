import React, { useState } from 'react';
import styled from 'styled-components';
import { ArrowLeft, Heart, CheckCircle } from 'lucide-react';
import { useNavigate, useParams } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';
import { donationApi } from '../services/api';

const PageContainer = styled.div`
  padding: 16px;
  max-width: 600px;
  margin: 0 auto;
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
  display: flex;
  align-items: center;
  justify-content: center;
`;

const Title = styled.h1`
  font-size: 24px;
  font-weight: 700;
  color: var(--tg-text-color, #000000);
  margin: 0;
`;

const FormContainer = styled.form`
  display: flex;
  flex-direction: column;
  gap: 16px;
`;

const FormGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 8px;
`;

const Label = styled.label`
  font-size: 14px;
  font-weight: 600;
  color: var(--tg-text-color, #000000);
`;

const Input = styled.input`
  padding: 12px 16px;
  border: 2px solid #e9ecef;
  border-radius: 12px;
  font-size: 16px;
  background: var(--tg-bg-color, #ffffff);
  color: var(--tg-text-color, #000000);
  transition: border-color 0.2s;

  &:focus {
    outline: none;
    border-color: #007bff;
  }

  &:disabled {
    background: #f8f9fa;
    cursor: not-allowed;
  }
`;

const TextArea = styled.textarea`
  padding: 12px 16px;
  border: 2px solid #e9ecef;
  border-radius: 12px;
  font-size: 16px;
  background: var(--tg-bg-color, #ffffff);
  color: var(--tg-text-color, #000000);
  min-height: 100px;
  resize: vertical;
  transition: border-color 0.2s;

  &:focus {
    outline: none;
    border-color: #007bff;
  }
`;

const AmountGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
`;

const AmountButton = styled.button<{ active?: boolean }>`
  padding: 12px;
  border: 2px solid ${props => props.active ? '#007bff' : '#e9ecef'};
  border-radius: 12px;
  background: ${props => props.active ? '#007bff' : 'var(--tg-bg-color, #ffffff)'};
  color: ${props => props.active ? '#ffffff' : 'var(--tg-text-color, #000000)'};
  font-size: 16px;
  font-weight: ${props => props.active ? 600 : 400};
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    border-color: #007bff;
  }
`;

const SubmitButton = styled.button`
  padding: 16px;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 8px;
  transition: transform 0.2s;

  &:hover {
    transform: translateY(-2px);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }
`;

const SuccessContainer = styled.div`
  text-align: center;
  padding: 40px 20px;
`;

const SuccessIcon = styled.div`
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 24px;
`;

const SuccessTitle = styled.h2`
  font-size: 24px;
  font-weight: 700;
  color: #28a745;
  margin-bottom: 16px;
`;

const SuccessMessage = styled.p`
  font-size: 16px;
  color: #6c757d;
  margin-bottom: 24px;
`;

const ButtonGroup = styled.div`
  display: flex;
  gap: 12px;
`;

const StyledButton = styled.button`
  padding: 12px 24px;
  border: 2px solid #e9ecef;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  flex: 1;
  transition: all 0.2s;

  ${props => props.color === 'primary' && `
    background: #007bff;
    color: white;
    border-color: #007bff;
    
    &:hover {
      background: #0056b3;
    }
  `}

  ${props => props.color === 'secondary' && `
    background: transparent;
    color: var(--tg-text-color, #000000);
    
    &:hover {
      background: #f8f9fa;
    }
  `}
`;

interface DonationFormData {
  name: string;
  phone: string;
  email: string;
  amount: number;
  purpose: string;
}

const DonationPage: React.FC = () => {
  const navigate = useNavigate();
  const { fundId } = useParams<{ fundId: string }>();
  const [showSuccess, setShowSuccess] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const { register, handleSubmit, setValue, watch, formState: { errors } } = useForm<DonationFormData>();
  
  const watchAmount = watch('amount');

  const quickAmounts = [100, 500, 1000, 3000, 5000];

  const handleQuickAmount = (amount: number) => {
    setValue('amount', amount);
  };

  const onSubmit = async (data: DonationFormData) => {
    setIsSubmitting(true);
    
    try {
      const response = await donationApi.createSimpleRequest({
        name: data.name,
        phone: data.phone,
        email: data.email || undefined,
        amount: data.amount.toString(),
        currency: 'RUB',
        fund_id: fundId ? parseInt(fundId) : undefined,
        purpose: data.purpose || undefined,
      });

      if (response.data.success) {
        setShowSuccess(true);
        toast.success(response.data.message || 'Заявка успешно отправлена!');
      } else {
        throw new Error(response.data.message || 'Ошибка при создании заявки');
      }
    } catch (error: any) {
      console.error('Error creating donation request:', error);
      
      // Детальная обработка ошибок
      if (error.response?.data?.detail) {
        toast.error(`Ошибка: ${error.response.data.detail}`);
      } else if (error.message) {
        toast.error(error.message);
      } else {
        toast.error('Ошибка при отправке заявки. Попробуйте позже.');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  if (showSuccess) {
    return (
      <PageContainer>
        <Header>
          <BackButton onClick={() => navigate('/funds')}>
            <ArrowLeft size={24} />
          </BackButton>
          <Title>Пожертвование</Title>
        </Header>

        <SuccessContainer>
          <SuccessIcon>
            <CheckCircle size={40} />
          </SuccessIcon>
          <SuccessTitle>Спасибо за заявку!</SuccessTitle>
          <SuccessMessage>
            Мы свяжемся с вами в ближайшее время для уточнения деталей пожертвования.
          </SuccessMessage>
          <ButtonGroup>
            <StyledButton color="primary" onClick={() => navigate('/funds')}>
              На главную
            </StyledButton>
            <StyledButton color="secondary" onClick={() => setShowSuccess(false)}>
              Еще одна заявка
            </StyledButton>
          </ButtonGroup>
        </SuccessContainer>
      </PageContainer>
    );
  }

  return (
    <PageContainer>
      <Header>
        <BackButton onClick={() => navigate('/funds')}>
          <ArrowLeft size={24} />
        </BackButton>
        <Title>Пожертвование</Title>
      </Header>

      <FormContainer onSubmit={handleSubmit(onSubmit)}>
        <FormGroup>
          <Label>Ваше имя *</Label>
          <Input
            type="text"
            placeholder="Введите ваше имя"
            {...register('name', { required: 'Имя обязательно' })}
          />
          {errors.name && <span style={{ color: '#dc3545', fontSize: '14px' }}>{errors.name.message}</span>}
        </FormGroup>

        <FormGroup>
          <Label>Телефон *</Label>
          <Input
            type="tel"
            placeholder="+7 (999) 123-45-67"
            {...register('phone', { 
              required: 'Телефон обязателен',
              pattern: {
                value: /^[\d\s+\-()]+$/,
                message: 'Введите корректный номер телефона'
              }
            })}
          />
          {errors.phone && <span style={{ color: '#dc3545', fontSize: '14px' }}>{errors.phone.message}</span>}
        </FormGroup>

        <FormGroup>
          <Label>Email</Label>
          <Input
            type="email"
            placeholder="email@example.com"
            {...register('email', {
              pattern: {
                value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                message: 'Введите корректный email'
              }
            })}
          />
          {errors.email && <span style={{ color: '#dc3545', fontSize: '14px' }}>{errors.email.message}</span>}
        </FormGroup>

        <FormGroup>
          <Label>Сумма пожертвования (₽) *</Label>
          <Input
            type="number"
            placeholder="Введите сумму"
            min="1"
            step="1"
            {...register('amount', { 
              required: 'Укажите сумму',
              min: { value: 1, message: 'Минимальная сумма 1 рубль' }
            })}
          />
          {errors.amount && <span style={{ color: '#dc3545', fontSize: '14px' }}>{errors.amount.message}</span>}
        </FormGroup>

        <AmountGrid>
          {quickAmounts.map(amount => (
            <AmountButton
              key={amount}
              type="button"
              active={watchAmount === amount}
              onClick={() => handleQuickAmount(amount)}
            >
              {amount}₽
            </AmountButton>
          ))}
        </AmountGrid>

        <FormGroup>
          <Label>Назначение пожертвования</Label>
          <TextArea
            placeholder="На что вы хотите пожертвовать? (необязательно)"
            {...register('purpose')}
          />
        </FormGroup>

        <SubmitButton type="submit" disabled={isSubmitting}>
          {isSubmitting ? (
            <>Отправка...</>
          ) : (
            <>
              <Heart size={20} />
              Отправить заявку
            </>
          )}
        </SubmitButton>
      </FormContainer>
    </PageContainer>
  );
};

export default DonationPage;
