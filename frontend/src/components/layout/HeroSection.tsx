import { PreferenceForm } from "@/components/form/PreferenceForm";
import type { FormOptions, PreferenceFormData } from "@/lib/types";

interface HeroSectionProps {
  options: FormOptions;
  form: PreferenceFormData;
  errors: string[];
  disabled?: boolean;
  onChange: (values: PreferenceFormData) => void;
  onSubmit: () => void;
}

export function HeroSection({
  options,
  form,
  errors,
  disabled,
  onChange,
  onSubmit,
}: HeroSectionProps) {
  return (
    <section className="hero-bg relative overflow-visible px-4 pb-16 pt-12 sm:px-6 sm:pb-20 sm:pt-16">
      <div className="mx-auto max-w-6xl overflow-visible">
        <div className="mx-auto max-w-3xl text-center">
          <h1 className="text-balance text-3xl font-extrabold tracking-tight text-white sm:text-4xl lg:text-5xl">
            What are you craving for?
          </h1>
          <p className="mt-4 text-balance text-base text-white/85 sm:text-lg">
            Tell us your mood and our AI will pick the perfect spot for you.
          </p>
        </div>

        <div className="mx-auto mt-10 max-w-3xl overflow-visible">
          <PreferenceForm
            options={options}
            values={form}
            errors={errors}
            disabled={disabled}
            onChange={onChange}
            onSubmit={onSubmit}
          />
        </div>
      </div>
    </section>
  );
}
