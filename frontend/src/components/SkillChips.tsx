import React from 'react';

interface Props {
  matchedSkills: string[];
  missingSkills: string[];
}

const CATEGORIES: Record<string, { label: string; keywords: string[] }> = {
  programming_languages: {
    label: 'Programming Languages',
    keywords: [
      'python', 'javascript', 'typescript', 'java', 'c++', 'c#', 'go', 'golang',
      'rust', 'ruby', 'php', 'swift', 'kotlin', 'scala', 'r', 'sql', 'html', 'css',
      'bash', 'shell'
    ]
  },
  frameworks_libraries: {
    label: 'Frameworks & Libraries',
    keywords: [
      'react', 'react.js', 'next.js', 'vue', 'vue.js', 'angular', 'node.js', 'express',
      'fastapi', 'flask', 'django', 'spring boot', 'dot net', 'asp.net', 'tailwind css',
      'bootstrap', 'shadcn', 'material ui', 'redux', 'zustand', 'graphql', 'rest api',
      'pandas', 'numpy', 'scikit-learn', 'sklearn', 'pytorch', 'tensorflow', 'keras',
      'sentence-transformers', 'transformers', 'langchain', 'llama-index', 'spacy', 'nltk',
      'opencv'
    ]
  },
  databases_storage: {
    label: 'Databases & Storage',
    keywords: [
      'postgresql', 'postgres', 'mysql', 'sqlite', 'mongodb', 'redis', 'firebase',
      'firestore', 'supabase', 'dynamodb', 'cassandra', 'elasticsearch', 'chromadb',
      'faiss', 'pinecone', 'qdrant', 'weaviate'
    ]
  },
  cloud_devops: {
    label: 'Cloud & DevOps',
    keywords: [
      'docker', 'kubernetes', 'k8s', 'aws', 'amazon web services', 'gcp', 'google cloud',
      'azure', 'terraform', 'ci/cd', 'github actions', 'gitlab ci', 'jenkins', 'nginx',
      'linux', 'ubuntu', 'helm'
    ]
  },
  tools_platforms: {
    label: 'Tools & Platforms',
    keywords: [
      'git', 'github', 'gitlab', 'bitbucket', 'jira', 'confluence', 'postman', 'figma',
      'vs code', 'docker desktop', 'celery', 'rabbitmq', 'kafka', 'spark', 'hadoop', 'airflow'
    ]
  },
  ai_ml_concepts: {
    label: 'AI & Machine Learning',
    keywords: [
      'natural language processing', 'nlp', 'machine learning', 'deep learning',
      'computer vision', 'llm', 'large language models', 'rag', 'retrieval-augmented generation',
      'embeddings', 'vector search', 'tf-idf', 'cosine similarity', 'prompt engineering',
      'supervised learning', 'unsupervised learning', 'reinforcement learning', 'fine-tuning',
      'bert'
    ]
  }
};

function getSkillCategory(skill: string): string {
  const normalized = skill.toLowerCase().trim();
  for (const [catId, catInfo] of Object.entries(CATEGORIES)) {
    if (catInfo.keywords.includes(normalized)) {
      return catId;
    }
  }
  return 'other';
}

const SkillChips: React.FC<Props> = ({ matchedSkills, missingSkills }) => {
  const groups: Record<string, { label: string; matched: string[]; missing: string[] }> = {
    programming_languages: { label: 'Programming Languages', matched: [], missing: [] },
    frameworks_libraries: { label: 'Frameworks & Libraries', matched: [], missing: [] },
    databases_storage: { label: 'Databases & Storage', matched: [], missing: [] },
    cloud_devops: { label: 'Cloud & DevOps', matched: [], missing: [] },
    tools_platforms: { label: 'Tools & Platforms', matched: [], missing: [] },
    ai_ml_concepts: { label: 'AI & Machine Learning', matched: [], missing: [] },
    other: { label: 'Other/General Skills', matched: [], missing: [] },
  };

  matchedSkills.forEach((skill) => {
    const cat = getSkillCategory(skill);
    groups[cat].matched.push(skill);
  });

  missingSkills.forEach((skill) => {
    const cat = getSkillCategory(skill);
    groups[cat].missing.push(skill);
  });

  const activeCategories = Object.entries(groups).filter(
    ([_, data]) => data.matched.length > 0 || data.missing.length > 0
  );

  return (
    <div className="glass-card p-6 space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-lg font-semibold text-white">Interactive Skill Gap Matrix</h3>
          <p className="text-xs text-slate-400">Comparing target job description requirements against resume skills</p>
        </div>
        <div className="flex gap-4 text-xs">
          <span className="flex items-center gap-1.5 text-emerald-400 font-medium">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-400/20 border border-emerald-400" />
            Matched ({matchedSkills.length})
          </span>
          <span className="flex items-center gap-1.5 text-red-400 font-medium">
            <span className="w-2.5 h-2.5 rounded-full bg-red-400/20 border border-red-400" />
            Missing ({missingSkills.length})
          </span>
        </div>
      </div>

      {activeCategories.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {activeCategories.map(([catKey, data]) => (
            <div key={catKey} className="p-4 rounded-xl bg-slate-900/30 border border-slate-800/80 hover:border-slate-700/60 transition-all flex flex-col justify-between">
              <div>
                <h4 className="text-sm font-bold text-slate-300 mb-3 flex items-center justify-between">
                  <span>{data.label}</span>
                  <span className="text-xs font-normal text-slate-500">
                    {data.matched.length} / {data.matched.length + data.missing.length} matched
                  </span>
                </h4>

                <div className="space-y-4">
                  {/* Matched in this category */}
                  {data.matched.length > 0 && (
                    <div>
                      <span className="text-[10px] uppercase tracking-wider text-emerald-500/80 font-bold block mb-1.5">Possessed</span>
                      <div className="flex flex-wrap gap-1.5">
                        {data.matched.map((skill) => (
                          <span
                            key={skill}
                            className="px-2.5 py-0.5 rounded-md text-xs font-medium bg-emerald-500/10 border border-emerald-500/20 text-emerald-300"
                          >
                            ✓ {skill}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Missing in this category */}
                  {data.missing.length > 0 && (
                    <div>
                      <span className="text-[10px] uppercase tracking-wider text-red-500/80 font-bold block mb-1.5">Lacking</span>
                      <div className="flex flex-wrap gap-1.5">
                        {data.missing.map((skill) => (
                          <span
                            key={skill}
                            className="px-2.5 py-0.5 rounded-md text-xs font-medium bg-red-500/10 border border-red-500/20 text-red-300"
                          >
                            + {skill}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <p className="text-sm text-slate-500 italic text-center py-6">No technical skills detected in the job description.</p>
      )}
    </div>
  );
};

export default SkillChips;
