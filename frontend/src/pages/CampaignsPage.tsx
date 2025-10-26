import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import { useForm } from 'react-hook-form';
import { 
  Target, 
  ArrowLeft, 
  Plus, 
  Calendar, 
  DollarSign, 
  Users, 
  TrendingUp,
  Image as ImageIcon,
  Globe,
  FileText
} from 'lucide-react';
import toast from 'react-hot-toast';
import telegramService from '../services/telegram';
import { campaignsApi } from '../services/api';

const CampaignsContainer = styled.div`
  padding: 20px 16px;
  max-width: 100%;
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

const TabsContainer = styled.div`
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
  border-bottom: 1px solid #e9ecef;
`;

const Tab = styled.button<{ active: boolean }>`
  padding: 12px 16px;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  color: ${props => props.active ? 'var(--tg-button-color, #007bff)' : '#6c757d'};
  border-bottom: 2px solid ${props => props.active ? 'var(--tg-button-color, #007bff)' : 'transparent'};
`;

const CampaignsGrid = styled.div`
  display: grid;
  gap: 16px;
  margin-bottom: 24px;
`;

const CampaignCard = styled.div`
  background: var(--tg-bg-color, #ffffff);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s ease;
  
  &:hover {
    transform: translateY(-2px);
  }
`;

const CampaignImage = styled.div<{ imageUrl?: string }>`
  width: 100%;
  height: 120px;
  border-radius: 12px;
  background: ${props => props.imageUrl ? `url(${props.imageUrl})` : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'};
  background-size: cover;
  background-position: center;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
`;

const CampaignTitle = styled.h3`
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--tg-text-color, #000000);
`;

const CampaignDescription = styled.p`
  font-size: 14px;
  color: #6c757d;
  margin-bottom: 16px;
  line-height: 1.4;
`;

const ProgressBar = styled.div`
  width: 100%;
  height: 8px;
  background: #e9ecef;
  border-radius: 4px;
  margin-bottom: 12px;
  overflow: hidden;
`;

const ProgressFill = styled.div<{ percentage: number }>`
  width: ${props => props.percentage}%;
  height: 100%;
  background: linear-gradient(90deg, #28a745, #20c997);
  transition: width 0.3s ease;
`;

const CampaignStats = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
`;

const StatItem = styled.div`
  text-align: center;
`;

const StatValue = styled.div`
  font-size: 16px;
  font-weight: 600;
  color: var(--tg-text-color, #000000);
`;

const StatLabel = styled.div`
  font-size: 12px;
  color: #6c757d;
`;

const CampaignActions = styled.div`
  display: flex;
  gap: 12px;
`;

const ActionButton = styled.button<{ variant?: 'primary' | 'secondary' }>`
  flex: 1;
  padding: 12px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: opacity 0.2s ease;
  
  ${props => props.variant === 'primary' ? `
    background: var(--tg-button-color, #007bff);
    color: var(--tg-button-text-color, #ffffff);
  ` : `
    background: #f8f9fa;
    color: var(--tg-text-color, #000000);
    border: 1px solid #e9ecef;
  `}
  
  &:hover {
    opacity: 0.9;
  }
`;

const CreateCampaignForm = styled.form`
  background: var(--tg-bg-color, #ffffff);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
`;

const FormGroup = styled.div`
  margin-bottom: 20px;
`;

const FormLabel = styled.label`
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: var(--tg-text-color, #000000);
`;

const FormInput = styled.input`
  width: 100%;
  padding: 12px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 16px;
  background-color: var(--tg-bg-color, #ffffff);
  color: var(--tg-text-color, #000000);
  
  &:focus {
    outline: none;
    border-color: var(--tg-button-color, #007bff);
  }
`;

const FormTextarea = styled.textarea`
  width: 100%;
  padding: 12px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 16px;
  background-color: var(--tg-bg-color, #ffffff);
  color: var(--tg-text-color, #000000);
  min-height: 100px;
  resize: vertical;
  
  &:focus {
    outline: none;
    border-color: var(--tg-button-color, #007bff);
  }
`;

const FormSelect = styled.select`
  width: 100%;
  padding: 12px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 16px;
  background-color: var(--tg-bg-color, #ffffff);
  color: var(--tg-text-color, #000000);
  
  &:focus {
    outline: none;
    border-color: var(--tg-button-color, #007bff);
  }
`;

const SubmitButton = styled.button`
  width: 100%;
  padding: 16px;
  border: none;
  border-radius: 12px;
  background: var(--tg-button-color, #007bff);
  color: var(--tg-button-text-color, #ffffff);
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s ease;
  
  &:hover {
    opacity: 0.9;
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
`;

const EmptyState = styled.div`
  text-align: center;
  padding: 40px 20px;
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

const CampaignsPage: React.FC = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState<'browse' | 'create'>('browse');
  const [campaigns, setCampaigns] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const { register, handleSubmit, formState: { errors } } = useForm();

  useEffect(() => {
    if (activeTab === 'browse') {
      loadCampaigns();
    }
  }, [activeTab]);

  const loadCampaigns = async () => {
    setIsLoading(true);
    try {
      // Mock данные для демонстрации
      const mockCampaigns = [
        {
          id: 1,
          title: "Строительство мечети в Казани",
          description: "Сбор средств на строительство новой мечети в центре Казани",
          category: "mosque",
          goal_amount: 5000000,
          collected_amount: 3200000,
          participants_count: 1247,
          banner_url: null,
          status: "active",
          end_date: "2025-12-31"
        },
        {
          id: 2,
          title: "Помощь сиротам в Дагестане",
          description: "Обеспечение детей-сирот одеждой, питанием и образованием",
          category: "orphans",
          goal_amount: 1000000,
          collected_amount: 750000,
          participants_count: 892,
          banner_url: null,
          status: "active",
          end_date: "2025-06-30"
        },
        {
          id: 3,
          title: "Медицинская помощь в Сирии",
          description: "Закупка лекарств и медицинского оборудования для больниц",
          category: "medical",
          goal_amount: 2000000,
          collected_amount: 2000000,
          participants_count: 2156,
          banner_url: null,
          status: "completed",
          end_date: "2025-03-15"
        }
      ];
      setCampaigns(mockCampaigns);
    } catch (error) {
      console.error('Error loading campaigns:', error);
      toast.error('Ошибка загрузки кампаний');
    } finally {
      setIsLoading(false);
    }
  };

  const onSubmit = async (data: any) => {
    setIsSubmitting(true);
    telegramService.hapticFeedback('impact', 'medium');

    try {
      // Здесь будет реальный API вызов
      console.log('Creating campaign:', data);
      toast.success('Кампания создана и отправлена на модерацию');
      setActiveTab('browse');
      loadCampaigns();
    } catch (error) {
      console.error('Error creating campaign:', error);
      toast.error('Ошибка создания кампании');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleCampaignClick = (campaignId: number) => {
    navigate(`/campaign/${campaignId}`);
  };

  const handleDonateClick = (campaignId: number, e: React.MouseEvent) => {
    e.stopPropagation();
    navigate(`/donate/campaign/${campaignId}`);
  };

  const getProgressPercentage = (collected: number, goal: number) => {
    return Math.min((collected / goal) * 100, 100);
  };

  const formatAmount = (amount: number) => {
    return new Intl.NumberFormat('ru-RU').format(amount) + ' ₽';
  };

  return (
    <CampaignsContainer>
      <Header>
        <BackButton onClick={() => navigate('/')}>
          <ArrowLeft size={24} />
        </BackButton>
        <Title>Целевые кампании</Title>
      </Header>

      <TabsContainer>
        <Tab 
          active={activeTab === 'browse'} 
          onClick={() => setActiveTab('browse')}
        >
          <Target size={16} style={{ marginRight: '8px' }} />
          Активные кампании
        </Tab>
        <Tab 
          active={activeTab === 'create'} 
          onClick={() => setActiveTab('create')}
        >
          <Plus size={16} style={{ marginRight: '8px' }} />
          Создать кампанию
        </Tab>
      </TabsContainer>

      {activeTab === 'browse' && (
        <>
          {isLoading ? (
            <EmptyState>
              <EmptyIcon>
                <Target size={32} />
              </EmptyIcon>
              <p>Загрузка кампаний...</p>
            </EmptyState>
          ) : campaigns.length === 0 ? (
            <EmptyState>
              <EmptyIcon>
                <Target size={32} />
              </EmptyIcon>
              <p>Нет активных кампаний</p>
              <p>Станьте первым, кто создаст кампанию!</p>
            </EmptyState>
          ) : (
            <CampaignsGrid>
              {campaigns.map((campaign) => (
                <CampaignCard 
                  key={campaign.id}
                  onClick={() => handleCampaignClick(campaign.id)}
                >
                  <CampaignImage imageUrl={campaign.banner_url}>
                    {!campaign.banner_url && <Target size={32} />}
                  </CampaignImage>
                  
                  <CampaignTitle>{campaign.title}</CampaignTitle>
                  <CampaignDescription>{campaign.description}</CampaignDescription>
                  
                  <ProgressBar>
                    <ProgressFill 
                      percentage={getProgressPercentage(campaign.collected_amount, campaign.goal_amount)}
                    />
                  </ProgressBar>
                  
                  <CampaignStats>
                    <StatItem>
                      <StatValue>{formatAmount(campaign.collected_amount)}</StatValue>
                      <StatLabel>из {formatAmount(campaign.goal_amount)}</StatLabel>
                    </StatItem>
                    <StatItem>
                      <StatValue>{campaign.participants_count}</StatValue>
                      <StatLabel>участников</StatLabel>
                    </StatItem>
                    <StatItem>
                      <StatValue>{Math.round(getProgressPercentage(campaign.collected_amount, campaign.goal_amount))}%</StatValue>
                      <StatLabel>прогресс</StatLabel>
                    </StatItem>
                  </CampaignStats>
                  
                  <CampaignActions>
                    <ActionButton 
                      variant="primary"
                      onClick={(e) => handleDonateClick(campaign.id, e)}
                    >
                      <DollarSign size={16} style={{ marginRight: '8px' }} />
                      Помочь
                    </ActionButton>
                    <ActionButton 
                      variant="secondary"
                      onClick={(e) => {
                        e.stopPropagation();
                        // Показать подробности
                      }}
                    >
                      <FileText size={16} style={{ marginRight: '8px' }} />
                      Подробнее
                    </ActionButton>
                  </CampaignActions>
                </CampaignCard>
              ))}
            </CampaignsGrid>
          )}
        </>
      )}

      {activeTab === 'create' && (
        <CreateCampaignForm onSubmit={handleSubmit(onSubmit)}>
          <FormGroup>
            <FormLabel>Название кампании *</FormLabel>
            <FormInput
              type="text"
              placeholder="Например: Строительство мечети в Казани"
              {...register('title', { required: 'Название обязательно' })}
            />
            {errors.title && <p style={{ color: '#dc3545', fontSize: '14px', marginTop: '4px' }}>{errors.title.message}</p>}
          </FormGroup>

          <FormGroup>
            <FormLabel>Описание *</FormLabel>
            <FormTextarea
              placeholder="Подробно опишите цель кампании, как будут использованы средства..."
              {...register('description', { required: 'Описание обязательно' })}
            />
            {errors.description && <p style={{ color: '#dc3545', fontSize: '14px', marginTop: '4px' }}>{errors.description.message}</p>}
          </FormGroup>

          <FormGroup>
            <FormLabel>Категория *</FormLabel>
            <FormSelect {...register('category', { required: 'Категория обязательна' })}>
              <option value="">Выберите категорию</option>
              <option value="mosque">Строительство мечети</option>
              <option value="orphans">Помощь сиротам</option>
              <option value="medical">Медицинская помощь</option>
              <option value="education">Образование</option>
              <option value="food">Продовольственная помощь</option>
              <option value="emergency">Экстренная помощь</option>
            </FormSelect>
            {errors.category && <p style={{ color: '#dc3545', fontSize: '14px', marginTop: '4px' }}>{errors.category.message}</p>}
          </FormGroup>

          <FormGroup>
            <FormLabel>Целевая сумма (₽) *</FormLabel>
            <FormInput
              type="number"
              placeholder="1000000"
              min="1000"
              max="10000000"
              {...register('goal_amount', { 
                required: 'Целевая сумма обязательна',
                min: { value: 1000, message: 'Минимум 1,000 ₽' },
                max: { value: 10000000, message: 'Максимум 10,000,000 ₽' }
              })}
            />
            {errors.goal_amount && <p style={{ color: '#dc3545', fontSize: '14px', marginTop: '4px' }}>{errors.goal_amount.message}</p>}
          </FormGroup>

          <FormGroup>
            <FormLabel>Срок сбора</FormLabel>
            <FormInput
              type="date"
              {...register('end_date')}
            />
          </FormGroup>

          <FormGroup>
            <FormLabel>Ссылка на изображение (опционально)</FormLabel>
            <FormInput
              type="url"
              placeholder="https://example.com/image.jpg"
              {...register('banner_url')}
            />
          </FormGroup>

          <SubmitButton type="submit" disabled={isSubmitting}>
            {isSubmitting ? 'Создаем кампанию...' : 'Создать кампанию'}
          </SubmitButton>
        </CreateCampaignForm>
      )}
    </CampaignsContainer>
  );
};

export default CampaignsPage;
