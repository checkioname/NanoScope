"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

export default function ButtonDialog({ onRun }) {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <motion.div className="w-1/5 relative">
      <AnimatePresence initial={false}>
        {!isExpanded && (
          <motion.button
            layoutId="run-button"
            className="w-full cursor-pointer bg-[#05675F] text-white font-bold rounded-lg px-8 py-4 shadow-lg"
            onClick={() => setIsExpanded(true)}
            initial={{ borderRadius: 12 }}
            animate={{ borderRadius: 12 }}
            exit={{ opacity: 0, scale: 0.95 }}
            whileHover={{
              scale: 1.05,
              boxShadow: "0px 0px 10px rgba(0,0,0,0.3)",
            }}
            transition={{ type: "spring", stiffness: 250, damping: 32 }}
          >
           Run 
          </motion.button>
        )}

        {isExpanded && (
          <motion.div
            layoutId="run-button"
            className="bg-[#05675F]/5 rounded-lg shadow-lg p-6 h-4/6"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1, borderRadius: 24 }}
            exit={{ opacity: 0 }}
            transition={{ type: "spring", stiffness: 200, damping: 40 }}
            style={{ minHeight: 150 }}
          >
            <div className="flex justify-between items-start mb-4">
              <h2 className="text-2xl font-semibold text-white/90">Confirm</h2>
              <button
                onClick={() => setIsExpanded(false)}
                aria-label="Close panel"
                className="text-white/40 hover:text-gray-900 font-bold text-2xl select-none"
              >
                &times;
              </button>
            </div>
            <br />
            {/* Aqui você pode colocar formulários, resultados e o que precisar */}
            {onRun && (
              <div className="w-full flex justify-between">
                <button
                  className="px-4 py-2 w-4/9 rounded-full bg-gray-500/50 text-white rounded hover:bg-[#044c48]"
                  onClick={onRun}
                >
                  Cancel
                </button>
                <button
                  className="px-4 py-2 w-4/9 rounded-full bg-[#05675F] text-white rounded hover:bg-[#044c48]"
                  onClick={onRun}
                >
                  Send
                </button>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}
