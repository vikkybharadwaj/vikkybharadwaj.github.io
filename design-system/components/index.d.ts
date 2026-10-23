type Tone = 'green' | 'blue' | 'purple' | 'amber' | 'teal' | 'cyan';

export interface ButtonProps { variant?: 'primary' | 'ghost'; href?: string; onClick?: () => void; children: React.ReactNode }
export interface EyebrowProps { variant?: 'box' | 'label'; tone?: Tone; children: React.ReactNode }
export interface PillProps { variant?: 'outline' | 'tint'; tone?: Tone | 'neutral'; href?: string; children: React.ReactNode }
export interface CardProps { tier?: 'primary' | 'secondary'; image?: string; imageAlt?: string; tone?: Tone; number?: string; title: React.ReactNode; subtitle?: string; tags?: string[]; href?: string; cta?: string; children?: React.ReactNode }
export interface StatProps { tone?: Tone; value: React.ReactNode; label: string; context?: string; caption?: string }
export interface CompanyMarkProps { name: string; description?: string; logo?: string; logoHasName?: boolean }
export interface ProofStatProps { tone?: Tone; value: React.ReactNode; label: string; from?: number; to?: number; context?: string }
export interface CalloutProps { tone?: Tone; title?: string; children: React.ReactNode }
export interface CodeBlockProps { prompt?: boolean; label?: string; children: React.ReactNode }
export interface NavProps { brand?: string; brandTail?: string; homeHref?: string; links?: { label: string; href: string; active?: boolean }[] }
