CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'run_status') THEN
    CREATE TYPE run_status AS ENUM ('Pending','Running','Failed','Completed');
  END IF;
END$$;

CREATE TABLE IF NOT EXISTS product (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL UNIQUE,
  enabled boolean NOT NULL DEFAULT true,
  cron text,
  status run_status NOT NULL DEFAULT 'Pending',
  last_updated timestamptz NOT NULL DEFAULT now(),
  metadata jsonb NOT NULL DEFAULT '{}'::jsonb
);
CREATE INDEX IF NOT EXISTS idx_product_enabled ON product (enabled);
CREATE INDEX IF NOT EXISTS idx_product_status ON product (status);
CREATE INDEX IF NOT EXISTS idx_product_metadata ON product USING GIN (metadata);

CREATE TABLE IF NOT EXISTS execution_history (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  product_id uuid NOT NULL REFERENCES product(id) ON DELETE CASCADE,
  name text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  status run_status NOT NULL DEFAULT 'Pending',
  pipeline_run_id text,
  duration_ms bigint,
  metadata jsonb NOT NULL DEFAULT '{}'::jsonb
);
CREATE INDEX IF NOT EXISTS idx_hist_status ON execution_history (status);
CREATE INDEX IF NOT EXISTS idx_hist_product ON execution_history (product_id);
CREATE INDEX IF NOT EXISTS idx_hist_created ON execution_history (created_at);

CREATE TABLE IF NOT EXISTS execution_step (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  history_id uuid NOT NULL REFERENCES execution_history(id) ON DELETE CASCADE,
  sequence int NOT NULL CHECK (sequence BETWEEN 1 AND 4),
  step_name text NOT NULL,
  scripting jsonb NOT NULL DEFAULT '{}'::jsonb,
  script_output jsonb NOT NULL DEFAULT '{}'::jsonb,
  status run_status NOT NULL DEFAULT 'Pending',
  started_at timestamptz,
  finished_at timestamptz,
  error_message text,
  metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
  UNIQUE (history_id, sequence)
);

CREATE OR REPLACE FUNCTION touch_updated_at() RETURNS trigger AS $$
BEGIN NEW.updated_at = now(); RETURN NEW; END $$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_hist_touch ON execution_history;
CREATE TRIGGER trg_hist_touch BEFORE UPDATE ON execution_history
FOR EACH ROW EXECUTE FUNCTION touch_updated_at();
