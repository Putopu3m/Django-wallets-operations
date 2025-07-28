import React from 'react'

export default function MainPage() {


    return (
        <div className="w-60 h-30 bg-gray-50 p-3 flex flex-col gap-1">
      
      <div className="flex flex-col gap-4">
        <div className="flex flex-row justify-between">
          <div className="flex flex-col">
            <span className="text-xl font-bold">Long Chair</span>
            <p className="text-xs text-gray-700">ID: 23432252</p>
          </div>
          <span className="font-bold text-red-600">$25.99</span>
        </div>
        <button className="hover:bg-sky-700 text-gray-50 bg-sky-800 py-2">Выбрать</button>
      </div>
    </div>
    )
}
