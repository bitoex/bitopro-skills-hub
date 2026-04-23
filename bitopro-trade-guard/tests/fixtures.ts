import type { StrategySession, PendingStep } from "../handler.ts";

type DeepPartial<T> = T extends object ? { [K in keyof T]?: DeepPartial<T[K]> } : T;

export function makeEvent(overrides: Record<string, any> = {}): any {
  return {
    type: "message",
    action: "preprocessed",
    sessionKey: "test-session",
    context: {
      content: "",
      bodyForAgent: ""
    },
    messages: [] as string[],
    ...overrides
  };
}

export function makeSession(overrides: DeepPartial<StrategySession> = {}): StrategySession {
  const now = new Date().toISOString();
  const thirtyDaysAhead = new Date(Date.now() + 30 * 24 * 3600 * 1000).toISOString();

  const defaults: StrategySession = {
    strategy_session_id: "test-s1",
    status: "approved",
    approved_at: now,
    policy: {
      max_steps: 30,
      max_total_exposure_quote: 90000,
      max_single_order_quote: 3000,
      max_daily_loss_quote: 5000,
      session_expiry_at: thirtyDaysAhead,
      on_escalation_timeout: { timeout_minutes: 30, action: "HALT_NO_NEW" }
    },
    risk_state: {
      current_step: 10,
      total_exposure_quote: 30000,
      realized_pnl_quote: 0,
      last_activity_at: now
    }
  };

  return {
    ...defaults,
    ...overrides,
    policy: { ...defaults.policy!, ...(overrides.policy ?? {}) } as StrategySession["policy"],
    risk_state: {
      ...defaults.risk_state!,
      ...(overrides.risk_state ?? {})
    } as StrategySession["risk_state"]
  };
}

export function makeSessionWithoutExpiry(
  overrides: DeepPartial<StrategySession> = {}
): StrategySession {
  const s = makeSession(overrides);
  if (s.policy) {
    const { session_expiry_at, ...rest } = s.policy;
    s.policy = rest as StrategySession["policy"];
  }
  return s;
}

export function pending(size_quote: number): PendingStep {
  return { size_quote };
}

export function hoursAgo(hours: number): string {
  return new Date(Date.now() - hours * 3600 * 1000).toISOString();
}

export function hoursAhead(hours: number): string {
  return new Date(Date.now() + hours * 3600 * 1000).toISOString();
}

export function daysAgo(days: number): string {
  return hoursAgo(days * 24);
}

export function daysAhead(days: number): string {
  return hoursAhead(days * 24);
}
