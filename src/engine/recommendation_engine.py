

import json
import random
from typing import Dict, List, Any, Tuple
from ..models.text_analyzer import TextAnalyzer

class RecommendationEngine:
    def __init__(self):
        """Initialize the recommendation engine"""
        self.text_analyzer = TextAnalyzer()
        
        # Technology stacks for different platforms
        self.tech_stacks = {
            'mobile': {
                'flutter': {
                    'name': 'Flutter + Firebase',
                    'description': 'Cross-platform mobile development with cloud backend',
                    'pros': ['Cross-platform', 'Fast development', 'Rich UI components'],
                    'cons': ['Limited native features', 'Large app size'],
                    'cost_factor': 1.0,
                    'timeline_factor': 1.0
                },
                'react_native': {
                    'name': 'React Native + Node.js',
                    'description': 'JavaScript-based mobile development',
                    'pros': ['Cross-platform', 'Large community', 'Reusable code'],
                    'cons': ['Performance issues', 'Native dependencies'],
                    'cost_factor': 0.9,
                    'timeline_factor': 1.1
                },
                'native_ios': {
                    'name': 'Swift + iOS Native',
                    'description': 'Native iOS development',
                    'pros': ['Best performance', 'Full iOS features', 'App Store optimization'],
                    'cons': ['iOS only', 'Higher cost', 'Longer timeline'],
                    'cost_factor': 1.3,
                    'timeline_factor': 1.4
                },
                'native_android': {
                    'name': 'Kotlin + Android Native',
                    'description': 'Native Android development',
                    'pros': ['Best performance', 'Full Android features', 'Google Play optimization'],
                    'cons': ['Android only', 'Higher cost', 'Longer timeline'],
                    'cost_factor': 1.2,
                    'timeline_factor': 1.3
                }
            },
            'web': {
                'mern': {
                    'name': 'MERN Stack (MongoDB, Express, React, Node.js)',
                    'description': 'Full-stack JavaScript development',
                    'pros': ['Fast development', 'Large ecosystem', 'Scalable'],
                    'cons': ['JavaScript everywhere', 'Learning curve'],
                    'cost_factor': 0.8,
                    'timeline_factor': 0.9
                },
                'mean': {
                    'name': 'MEAN Stack (MongoDB, Express, Angular, Node.js)',
                    'description': 'Full-stack JavaScript with Angular',
                    'pros': ['TypeScript support', 'Enterprise-ready', 'Comprehensive framework'],
                    'cons': ['Steep learning curve', 'Heavy framework'],
                    'cost_factor': 1.0,
                    'timeline_factor': 1.1
                },
                'django': {
                    'name': 'Django + PostgreSQL',
                    'description': 'Python-based web development',
                    'pros': ['Rapid development', 'Built-in admin', 'Security features'],
                    'cons': ['Less flexible', 'Monolithic'],
                    'cost_factor': 0.9,
                    'timeline_factor': 0.8
                },
                'laravel': {
                    'name': 'Laravel + MySQL',
                    'description': 'PHP-based web development',
                    'pros': ['Elegant syntax', 'Rich ecosystem', 'Easy deployment'],
                    'cons': ['PHP ecosystem', 'Performance concerns'],
                    'cost_factor': 0.7,
                    'timeline_factor': 0.9
                }
            },
            'desktop': {
                'electron': {
                    'name': 'Electron + React',
                    'description': 'Cross-platform desktop development',
                    'pros': ['Cross-platform', 'Web technologies', 'Rapid development'],
                    'cons': ['Large app size', 'Memory usage', 'Security concerns'],
                    'cost_factor': 0.8,
                    'timeline_factor': 0.9
                },
                'qt': {
                    'name': 'Qt + Python',
                    'description': 'Native desktop development',
                    'pros': ['Native performance', 'Cross-platform', 'Rich UI'],
                    'cons': ['Complex setup', 'Licensing costs'],
                    'cost_factor': 1.1,
                    'timeline_factor': 1.2
                },
                'wpf': {
                    'name': 'WPF + C#',
                    'description': 'Windows desktop development',
                    'pros': ['Native Windows', 'Rich UI', 'Good performance'],
                    'cons': ['Windows only', 'Microsoft ecosystem'],
                    'cost_factor': 1.0,
                    'timeline_factor': 1.0
                }
            }
        }
        
        # Feature recommendations by business type
        self.business_features = {
            'retail': [
                'inventory_management', 'payment_processing', 'order_tracking',
                'customer_management', 'analytics_dashboard', 'multi_vendor_support'
            ],
            'restaurant': [
                'menu_management', 'online_ordering', 'delivery_tracking',
                'reservation_system', 'kitchen_display', 'loyalty_program'
            ],
            'healthcare': [
                'patient_management', 'appointment_scheduling', 'medical_records',
                'billing_system', 'prescription_management', 'telemedicine'
            ],
            'education': [
                'course_management', 'student_portal', 'progress_tracking',
                'video_streaming', 'assignment_submission', 'grade_management'
            ],
            'logistics': [
                'route_optimization', 'real_time_tracking', 'inventory_management',
                'driver_app', 'warehouse_management', 'analytics_dashboard'
            ],
            'finance': [
                'account_management', 'transaction_history', 'budget_tracking',
                'financial_reports', 'investment_portfolio', 'loan_management'
            ],
            'real_estate': [
                'property_listings', 'search_filters', 'virtual_tours',
                'contact_forms', 'lead_management', 'property_analytics'
            ],
            'consulting': [
                'project_management', 'time_tracking', 'client_billing',
                'report_generation', 'resource_management', 'knowledge_base'
            ]
        }
        
        # Feature descriptions
        self.feature_descriptions = {
            'inventory_management': 'Track and manage product inventory in real-time',
            'payment_processing': 'Secure payment processing with multiple payment methods',
            'order_tracking': 'Real-time order status tracking for customers',
            'customer_management': 'Comprehensive customer database and relationship management',
            'analytics_dashboard': 'Business intelligence and performance analytics',
            'multi_vendor_support': 'Support for multiple vendors and suppliers',
            'menu_management': 'Dynamic menu creation and management system',
            'online_ordering': 'Online food ordering and delivery system',
            'delivery_tracking': 'Real-time delivery tracking for customers',
            'reservation_system': 'Table reservation and booking management',
            'kitchen_display': 'Kitchen order display and management system',
            'loyalty_program': 'Customer loyalty and rewards program',
            'patient_management': 'Comprehensive patient information management',
            'appointment_scheduling': 'Automated appointment booking and scheduling',
            'medical_records': 'Secure electronic health records management',
            'billing_system': 'Automated billing and insurance processing',
            'prescription_management': 'Digital prescription and medication tracking',
            'telemedicine': 'Video consultation and remote healthcare services',
            'course_management': 'Learning management system for courses',
            'student_portal': 'Student dashboard and self-service portal',
            'progress_tracking': 'Student progress monitoring and assessment',
            'video_streaming': 'Educational video content delivery',
            'assignment_submission': 'Digital assignment submission and grading',
            'grade_management': 'Automated grading and transcript management',
            'route_optimization': 'AI-powered route planning and optimization',
            'real_time_tracking': 'GPS-based real-time location tracking',
            'driver_app': 'Mobile application for drivers and delivery personnel',
            'warehouse_management': 'Inventory and warehouse operations management',
            'account_management': 'Banking account and transaction management',
            'transaction_history': 'Detailed transaction history and statements',
            'budget_tracking': 'Personal and business budget management',
            'financial_reports': 'Comprehensive financial reporting and analytics',
            'investment_portfolio': 'Investment tracking and portfolio management',
            'loan_management': 'Loan application and management system',
            'property_listings': 'Real estate property listing and showcase',
            'search_filters': 'Advanced property search and filtering',
            'virtual_tours': '360-degree virtual property tours',
            'contact_forms': 'Lead capture and contact management',
            'lead_management': 'Sales lead tracking and management',
            'property_analytics': 'Real estate market analytics and insights',
            'project_management': 'Comprehensive project planning and tracking',
            'time_tracking': 'Employee time tracking and billing',
            'client_billing': 'Automated client billing and invoicing',
            'report_generation': 'Automated report generation and delivery',
            'resource_management': 'Team and resource allocation management',
            'knowledge_base': 'Documentation and knowledge management system',
            'tracking': 'Real-time activity and data tracking with analytics'
        }

    def generate_recommendation(self, client_input: str, additional_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate comprehensive recommendation based on client input"""
        # Analyze the input text
        analysis = self.text_analyzer.analyze_text(client_input)
        
        # Determine if clarification is needed
        needs_clarification = self.text_analyzer.needs_clarification(analysis)
        clarification_questions = self.text_analyzer.generate_clarification_questions(analysis)
        
        # Generate recommendations
        platform_rec =  self._recommend_platform(analysis, additional_info)
        features_rec = self._recommend_features(analysis, additional_info)
        tech_stack_rec = self._recommend_tech_stack(platform_rec, analysis, additional_info)
        cost_estimate = self._estimate_cost(platform_rec, features_rec, tech_stack_rec, additional_info)
        timeline_estimate = self._estimate_timeline(platform_rec, features_rec, tech_stack_rec, additional_info)
        
        recommendation = {
            'input_analysis': analysis,
            'needs_clarification': needs_clarification,
            'clarification_questions': clarification_questions,
            'platform_recommendation': platform_rec,
            'feature_recommendations': features_rec,
            'tech_stack_recommendation': tech_stack_rec,
            'cost_estimate': cost_estimate,
            'timeline_estimate': timeline_estimate,
            'confidence_score': self._calculate_confidence(analysis, platform_rec, features_rec)
        }
        
        return recommendation

    def _recommend_platform(self, analysis: Dict[str, Any], additional_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """Recommend the best platform (mobile/web/desktop)"""
       
        platform_pref, platform_confidence = analysis['platform_preference']
        
        # Consider additional info first if provided
        #if additional_info and 'portability_requirement' in additional_info:
        portability = additional_info['portability_requirement']
        business_type = additional_info['business_type']
        access = additional_info['access_requirement']
        #portability = analysis.get('portability', '').lower()
        notification_requirement = analysis.get('notification_requirement', '').lower()
        
        if portability  == 'high' or notification_requirement=='major':
                return {
                    'type':business_type,
                    'platform': 'mobile',
                    'confidence': 0.95,
                    'reasoning': f"Mobile recommended due to high portability requirement"
                }
        elif portability == 'low' or access=='offline':
                return {
                      'type':business_type,
                'platform': 'desktop',
                    'confidence': 0.9,
                    'reasoning': f"Desktop recommended due to low portability requirement"
               
                }
        else:  
                return {
                      'type':business_type,
                      'platform':  platform_pref,
                    'confidence': 0.9,
                    'reasoning': f"{ platform_pref.title()} recommended due to medium portability requirement"
                }
        
        # Check for portability and notification requirements from analysis
       
    
        
        # Use business type to determine optimal platform
        platform_mapping = {
            'retail': 'web',
            'restaurant': 'mobile',
            'healthcare': 'mobile',
            'education': 'web',
            'logistics': 'mobile',
            'finance': 'web',
            'real_estate': 'web',
            'consulting': 'desktop',
            'fitness': 'mobile',
            'entertainment': 'mobile',
            'transportation': 'mobile',
            'beauty': 'mobile',
            'pet_care': 'mobile',
            'childcare': 'mobile',
            'event_planning': 'mobile',
            'coffee_shop': 'mobile',
            'delivery': 'mobile',
            'travel': 'mobile',
            'pharmaceutical': 'mobile',
            'home_services': 'mobile',
            'music': 'mobile',
            'photography': 'mobile',
            'gaming': 'mobile',
            'automotive': 'mobile',
            'agriculture': 'mobile',
            'carpooling': 'mobile',
            'bike_sharing': 'mobile',
            'parking': 'mobile',
            'package_locker': 'mobile',
            'karaoke': 'mobile',
            'running': 'mobile',
            'language_exchange': 'mobile',
            'retirement_planning': 'mobile',
            'property_investment': 'mobile',
            'symptom_checker': 'mobile',
            'sleep_tracking': 'mobile',
            'cryptocurrency': 'mobile',
            'grocery_delivery': 'mobile',
            'medication_interaction': 'mobile',
            'music_production': 'mobile',
            'fashion_styling': 'mobile',
            'makeup_tutorial': 'mobile',
            'property_inspection': 'mobile',
            'dental_appointment': 'mobile',
            'credit_card_management': 'mobile',
            'beauty_product_recommendation': 'mobile',
            'car_maintenance': 'mobile',
            'language_learning': 'mobile',
            'loyalty_program': 'mobile',
            'tax_preparation': 'mobile',
            'mental_health': 'mobile',
            'podcast': 'mobile',
            'yoga': 'mobile',
            'budgeting': 'mobile',
            'nutrition_tracking': 'mobile',
            'workout_tracking': 'mobile',
            'medication_reminder': 'mobile',
            'salon_appointment': 'mobile',
            'farm_management': 'mobile',
            'personal_shopping': 'mobile',
            'swimming': 'mobile',
            'fleet_management': 'mobile',
            'public_transportation': 'mobile',
            'ride_sharing': 'mobile',
            'food_delivery': 'mobile',
            'telemedicine': 'mobile',
            'gym_management': 'mobile',
            'restaurant_reservation': 'mobile',
            'coffee_shop_ordering': 'mobile',
            'daycare_management': 'mobile',
            'event_management': 'mobile',
            'travel_booking': 'mobile',
            'warehouse_management': 'desktop',
            'hospital_management': 'desktop',
            'banking_system': 'desktop',
            'construction_project': 'desktop',
            'consulting_crm': 'desktop',
            'insurance_claims': 'desktop',
            'accounting_software': 'desktop',
            'manufacturing_quality': 'desktop',
            'architecture_project': 'desktop',
            'consulting_time_tracking': 'desktop',
            'real_estate_property': 'desktop',
            'finance_trading': 'desktop',
            'medical_imaging': 'desktop',
            'laboratory_information': 'desktop',
            'academic_research': 'desktop',
            'library_management': 'desktop',
            'loan_management': 'desktop',
            'school_management': 'desktop',
            'warehouse_automation': 'desktop',
            'customs_clearance': 'desktop',
            'quality_control': 'desktop',
            'property_valuation': 'desktop',
            'student_assessment': 'desktop',
            'pharmacy_management': 'desktop',
            'supply_chain': 'desktop',
            'medical_billing': 'desktop',
            'plagiarism_detection': 'desktop',
            'video_editing': 'web',
            'virtual_classroom': 'web',
            'property_marketing': 'web',
            'research_collaboration': 'web',
            'streaming_platform': 'web',
            'news_platform': 'web',
            'online_learning': 'web',
            'ecommerce_website': 'web',
            'content_management': 'web',
            'online_exam': 'web',
            'student_information': 'web',
            'property_listing': 'web',
            'video_production': 'web',
            'academic_research_platform': 'web'
        }
        
        recommended_platform = platform_mapping.get(business_type, 'web')
        
        # Override with user preference if high confidence
        if platform_confidence > 0.7:
            recommended_platform = platform_pref
        
        return {
            'platform': recommended_platform,
            'confidence': max(confidence, platform_confidence),
            'reasoning': f"Recommended {recommended_platform} based on business type ({business_type}) and user preferences"
        }

    def _recommend_features(self, analysis: Dict[str, Any], additional_info: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Recommend features based on detected features or business type"""
        business_type = additional_info['business_type']
        detected_features = analysis['detected_features']
        feature_recommendations = []
        if detected_features:
            # Only recommend detected features
            for feature in detected_features:
                feature_rec = {
                    'feature': feature,
                    'description': self.feature_descriptions.get(feature, 'None'),
                    'priority': 'high',
                    'estimated_effort': random.randint(2, 8),
                    'estimated_cost': random.randint(1000, 5000)
                }
                feature_recommendations.append(feature_rec)
            
        base_features = self.business_features.get(business_type, [])[:3]
        for feature in base_features:
                feature_rec = {
                    'feature': feature,
                    'description': self.feature_descriptions.get(feature, 'Feature description not available'),
                    'priority': 'medium',
                    'estimated_effort': random.randint(2, 8),
                    'estimated_cost': random.randint(1000, 5000)
                }
                feature_recommendations.append(feature_rec)
        # Add features from additional info if provided
        if additional_info and 'requested_features' in additional_info:
            for feature in additional_info['requested_features']:
                if feature not in [f['feature'] for f in feature_recommendations]:
                    feature_rec = {
                        'feature': feature,
                        'description': self.feature_descriptions.get(feature, 'Feature description not available'),
                        'priority': 'medium',
                        'estimated_effort': random.randint(2, 8),
                        'estimated_cost': random.randint(1000, 5000)
                    }
                    feature_recommendations.append(feature_rec)
        return feature_recommendations

    def _recommend_tech_stack(self, platform_rec: Dict[str, Any], analysis: Dict[str, Any], additional_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """Recommend technology stack based on platform and requirements"""
        platform = platform_rec['platform']
        business_type = additional_info['business_type']
        
        # Get available tech stacks for the platform
        available_stacks = self.tech_stacks.get(platform, {})
        
        if not available_stacks:
            return {
                'tech_stack': 'Unknown',
                'description': 'No technology stack available for this platform',
                'pros': [],
                'cons': [],
                'confidence': 0.0
            }
        
        # Select the best tech stack based on business type and requirements
        if platform == 'mobile':
            if business_type in ['restaurant', 'logistics']:
                recommended_stack = 'flutter'  # Good for delivery apps
            elif business_type in ['healthcare', 'finance']:
                recommended_stack = 'react_native'  # Good for enterprise apps
            else:
                recommended_stack = 'flutter'  # Default for mobile
        elif platform == 'web':
            if business_type in ['retail', 'real_estate']:
                recommended_stack = 'mern'  # Good for e-commerce
            elif business_type in ['healthcare', 'finance']:
                recommended_stack = 'django'  # Good for security
            elif business_type in ['education']:
                recommended_stack = 'laravel'  # Good for content management
            else:
                recommended_stack = 'mern'  # Default for web
        else:  # desktop
            recommended_stack = 'electron'  # Default for desktop
        
        # Override with additional info if provided
        if additional_info and 'tech_stack_preference' in additional_info:
            recommended_stack = additional_info['tech_stack_preference']
        
        tech_stack_info = available_stacks.get(recommended_stack, available_stacks[list(available_stacks.keys())[0]])
        
        return {
            'tech_stack': recommended_stack,
            'name': tech_stack_info['name'],
            'description': tech_stack_info['description'],
            'pros': tech_stack_info['pros'],
            'cons': tech_stack_info['cons'],
            'cost_factor': tech_stack_info['cost_factor'],
            'timeline_factor': tech_stack_info['timeline_factor'],
            'confidence': platform_rec['confidence']
        }

    def _estimate_cost(self, platform_rec: Dict[str, Any], features_rec: List[Dict[str, Any]], tech_stack_rec: Dict[str, Any], additional_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """Estimate project cost"""
        base_cost = {
            'mobile': 15000,
            'web': 12000,
            'desktop': 10000
        }
        
        platform = platform_rec['platform']
        base_platform_cost = base_cost.get(platform, 12000)
        
        # Add feature costs
        feature_cost = sum(feature['estimated_cost'] for feature in features_rec)
        
        # Apply tech stack cost factor
        tech_stack_cost_factor = tech_stack_rec.get('cost_factor', 1.0)
        
        # Apply business type multiplier
        business_multipliers = {
            'healthcare': 1.3,  # Higher due to compliance
            'finance': 1.4,     # Higher due to security
            'logistics': 1.2,   # Higher due to complexity
            'retail': 1.0,      # Standard
            'restaurant': 0.9,  # Slightly lower
            'education': 1.1,   # Slightly higher
            'real_estate': 1.0, # Standard
            'consulting': 0.9   # Slightly lower
        }
        
        business_type, _ = platform_rec.get('business_type', ('retail', 0.5))
        business_multiplier = business_multipliers.get(business_type, 1.0)
        
        # Calculate total cost
        total_cost = (base_platform_cost + feature_cost) * tech_stack_cost_factor * business_multiplier
        
        # Apply additional info if provided
        if additional_info and 'budget_constraint' in additional_info:
            total_cost = min(total_cost, additional_info['budget_constraint'])
        
        return {
            'base_cost': base_platform_cost,
            'feature_cost': feature_cost,
            'total_cost': round(total_cost, 2),
            'cost_range': f"${round(total_cost * 0.8, 2)} - ${round(total_cost * 1.2, 2)}",
            'currency': 'USD'
        }

    def _estimate_timeline(self, platform_rec: Dict[str, Any], features_rec: List[Dict[str, Any]], tech_stack_rec: Dict[str, Any], additional_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """Estimate project timeline"""
        base_timeline = {
            'mobile': 12,  # weeks
            'web': 10,     # weeks
            'desktop': 8   # weeks
        }
        
        platform = platform_rec['platform']
        base_platform_timeline = base_timeline.get(platform, 10)
        
        # Add feature timeline
        feature_timeline = sum(feature['estimated_effort'] for feature in features_rec)
        
        # Apply tech stack timeline factor
        tech_stack_timeline_factor = tech_stack_rec.get('timeline_factor', 1.0)
        
        # Calculate total timeline
        total_timeline = (base_platform_timeline + feature_timeline) * tech_stack_timeline_factor
        
        # Apply additional info if provided
        if additional_info and 'timeline_constraint' in additional_info:
            total_timeline = min(total_timeline, additional_info['timeline_constraint'])
        
        return {
            'base_timeline': base_platform_timeline,
            'feature_timeline': feature_timeline,
            'total_timeline': round(total_timeline, 1),
            'timeline_range': f"{round(total_timeline * 0.8, 1)} - {round(total_timeline * 1.2, 1)} weeks",
            'unit': 'weeks'
        }

    def _calculate_confidence(self, analysis: Dict[str, Any], platform_rec: Dict[str, Any], features_rec: List[Dict[str, Any]]) -> float:
        """Calculate confidence score for the recommendation"""
        clarity_score = analysis['clarity_score']
        business_type, business_confidence = analysis['business_type']
        platform_confidence = platform_rec['confidence']
        
        # Calculate confidence based on multiple factors
        confidence_factors = [
            clarity_score * 0.3,
            business_confidence * 0.3,
            platform_confidence * 0.2,
            min(1.0, len(features_rec) / 10) * 0.2  # More features = higher confidence
        ]
        
        total_confidence = sum(confidence_factors)
        return round(total_confidence, 2) 