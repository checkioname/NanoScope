"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

export default function ButtonDialog() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <AnimatePresence initial={false}>
        {!isOpen && (
          <motion.button
            key="run-button"
            layoutId="run-button"
            className="w-36 flex items-center justify-center cursor-pointer bg-[#05675F] px-6 py-3 rounded-full text-white font-semibold shadow-lg"
            onClick={() => setIsOpen(true)}
            exit={{ opacity: 0, scale: 0.95 }}
            initial={{ borderRadius: 24 }}
            animate={{ borderRadius: 24 }}
            whileHover={{
              scale: 1.05,
              boxShadow: "0px 0px 10px rgba(0,0,0,0.3)",
            }}
            transition={{ type: "spring", stiffness: 350, damping: 32 }}
          >
            Run
          </motion.button>
        )}

        {isOpen && (
          <>
            {/* Backdrop */}
            <motion.div
              key="backdrop"
              className="fixed inset-0 bg-black/10 z-40 backdrop-blur-lg"
              initial={{ opacity: 0 }}
              animate={{ opacity: 0.8 }}
              exit={{ opacity: 0 }}
              onClick={() => setIsOpen(false)}
            />

            {/* Dialog com layoutId igual para transição */}
            <motion.div
              key="dialog"
              layoutId="run-button"
              className="fixed z-50 top-4/6 left-5/7 w-[320px] max-w-full bg-[#05675F]/90 rounded-2xl p-6 shadow-lg"
              style={{ transform: "translate(-10%, -10%)" }}
              initial={{ opacity: 0, borderRadius: 20 }}
              animate={{ opacity: 1, borderRadius: 26 }}
              exit={{ opacity: 0 }}
              transition={{ type: "spring", stiffness: 180, damping: 24 }}
              onClick={(e) => e.stopPropagation()} // evitar fechar quando clicar dentro
            >
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-semibold text-white">Confirm</h2>
                <button
                  onClick={() => setIsOpen(false)}
                  aria-label="Close dialog"
                  className="text-white hover:text-gray-200 font-bold text-2xl select-none"
                >
                  &times;
                </button>
              </div>

              <p className="text-white mb-6">
                Do you confirm the information provided?
              </p>

              <div className="flex gap-4">
                <button
                  className="flex-1 rounded-full border border-white/50 px-4 py-2 text-white
                    hover:bg-white hover:text-[#05675F] transition"
                  onClick={() => setIsOpen(false)}
                >
                  Cancel
                </button>

                <button
                  className="flex-1 rounded-full bg-[#05675F] px-4 py-2 text-white hover:bg-[#044c48] transition"
                  onClick={() => alert("Received!")}
                >
                  Run
                </button>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  );
}
