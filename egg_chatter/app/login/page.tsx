"use client"

import LongButton from "@/components/LongButton";
import Image from "next/image";
import { useRouter } from "next/navigation";

const Login = () => {
    const router = useRouter()

    const moveTo = () => {
        const params = new URLSearchParams({ step: "1" });
        router.push(`/profile?${params.toString()}`)
    }

    return(
        <div>
            {/* 에그채터 로고 */}
            <div className="flex justify-center items-center mt-36">
            <Image 
                src='/assets/logo.png' 
                alt="로고" 
                width={240} 
                height={0}
                className="drop-shadow-lg"
                />
            </div>

            {/* 에그체터 소개 */}
            <div className="text-center">
                <p className="text-4xl font-semibold mt-6">EggChatter</p>
                <p className="mt-4 text-[#969797]">대화 속 숨겨진 즐거움, 이스터에그를 찾아보세요!</p>
            </div>
            
            
            <LongButton text="카카오 로그인" onClick={moveTo}/>
            
        </div>
    )
}

export default Login