'use client';

import { motion } from 'framer-motion';
import { BookText, Database, Search } from 'lucide-react';

import type { Analytics, SourceItem } from '@/lib/types';
import { Badge } from '@/components/ui/badge';
import { Card } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';

type SourcesPanelProps = {
  sources: SourceItem[];
  analytics: Analytics | null;
};

export function SourcesPanel({ sources, analytics }: SourcesPanelProps) {
  return (
    <Card className='flex h-[calc(100vh-2rem)] flex-col p-4'>
      <h3 className='text-lg font-semibold'>Sources</h3>
      <p className='mt-1 text-xs text-muted-foreground'>Evidence used for the current answer.</p>

      <div className='mt-4 grid grid-cols-2 gap-2'>
        <div className='rounded-2xl border border-border bg-card/40 p-3'>
          <p className='text-xs text-muted-foreground'>Documents</p>
          <p className='mt-1 text-xl font-semibold'>{analytics?.document_count ?? 0}</p>
          <Database className='mt-2 h-4 w-4 text-muted-foreground' />
        </div>
        <div className='rounded-2xl border border-border bg-card/40 p-3'>
          <p className='text-xs text-muted-foreground'>Queries</p>
          <p className='mt-1 text-xl font-semibold'>{analytics?.query_count ?? 0}</p>
          <Search className='mt-2 h-4 w-4 text-muted-foreground' />
        </div>
      </div>

      <ScrollArea className='mt-4 flex-1'>
        <div className='space-y-3 pr-2'>
          {sources.map((source, idx) => (
            <motion.div
              key={`${source.document_name}-${source.page_number}-${idx}`}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              className='rounded-2xl border border-border bg-card/50 p-3'
            >
              <div className='flex items-center justify-between gap-2'>
                <div className='min-w-0'>
                  <p className='truncate text-sm font-semibold'>{source.document_name}</p>
                  <p className='text-xs text-muted-foreground'>Page {source.page_number}</p>
                </div>
                <Badge variant='outline'>{source.score.toFixed(3)}</Badge>
              </div>
              <p className='mt-2 line-clamp-6 text-xs text-muted-foreground'>{source.text}</p>
            </motion.div>
          ))}

          {!sources.length ? (
            <div className='rounded-2xl border border-dashed border-border p-6 text-center'>
              <BookText className='mx-auto h-5 w-5 text-muted-foreground' />
              <p className='mt-2 text-sm text-muted-foreground'>No sources yet. Run a query to inspect evidence.</p>
            </div>
          ) : null}
        </div>
      </ScrollArea>
    </Card>
  );
}
