"use client"

import LongButton from "@/components/LongButton";
import PageIndicator from "@/components/PageIndicator";
import ProfileArea from "@/components/ProfileArea";
import { ButtonBase, TextField } from "@mui/material";
import Image from "next/image";
import { useRouter, useSearchParams } from "next/navigation";
import { useState } from "react";
import { useEasterEggStore } from "../store";

const ProfileList = [
    {alt : "ecstatic", src : "/assets/ecstatic.png"},
    {alt : "bad", src : "/assets/bad.png"},
    {alt : "crying", src : "/assets/crying.png"},
    {alt : "angry", src : "/assets/angry.png"},
    {alt : "coll", src : "/assets/cool.png"},
    {alt : "happy", src : "/assets/happy.png"},
    {alt : "neutral", src : "/assets/neutral.png"},
    {alt : "smile", src : "/assets/smile.png"},
    {alt : "sad", src : "/assets/sad.png"},
]

const EasterEgg = () => {
    const searchParam = useSearchParams()
    const step = searchParam.get("step")
    const profile = useEasterEggStore((state) => state.profile)
    
    return (
        <div>
            {/* 페이지 인디케이터 */}
            <PageIndicator text="프로필"/>

            {/* 프로필 이미지 영역 */}
            <ProfileArea profile={profile}/>

            {/* 작성 영역 */}
            {step === "1" ? <ProfileImage/> : <NickName/>}
        </div>
    )
}

const ProfileImage = () => {
    const router = useRouter()
    const profile = useEasterEggStore((state) => state.profile)
    const setProfile = useEasterEggStore((state) => state.setProfile)

    const selectProfileImage = (src:string) => {
        setProfile(src)
    }

    const checkProfile = () => {
        if(profile === "" || profile === "/assets/user.png"){
            alert("프로필 이모지를 선택해 주세요.")
            return false
        }

        return true
    }
    
    const moveTo = () => {
        if(checkProfile()){
            const params = new URLSearchParams({ step: "2" });
            router.push(`?${params.toString()}`)
        }
    }

    return(
        <div className="flex justify-center py-4">
            <div className="grid grid-cols-3 gap-12">
                {ProfileList.map((prof, idx) => (
                    <ButtonBase onClick={() => selectProfileImage(prof.src)}
                    key={`${idx}-${prof.alt}`}>
                        <Image
                            src={prof.src}
                            alt={prof.alt}
                            width={64}
                            height={64}
                            className={profile != prof.src ? "opacity-45" : ""}
                        />
                    </ButtonBase>
                ))}
            </div>
            
            <LongButton text="확인" onClick={moveTo}/>
        </div>
    )
}

const NickName = () => {
    const nickname = useEasterEggStore((state) => state.nickname)
    const setNickname = useEasterEggStore((state) => state.setNickname)
    const setProfile = useEasterEggStore((state) => state.setProfile)
    const [error, setError] = useState(false)

    const handleChange = (e:React.ChangeEvent<HTMLInputElement>) => {
        const { target : { value } } = e

        if (value.length > 8) {
            setError(true)
        } else {
            setError(false)
        }

        setNickname(value)
    }

    const updateUserInfo = async() => {
        // await axios
        alert("프로필 등록 완료")
        setProfile("/assets/user.png")
        setNickname("")
    }

    return (
        <div className="flex justify-center">
            <TextField
                required
                id="outlined-required"
                label="닉네임"
                value={nickname}
                error={error}
                helperText={error ? "닉네임은 8글자 이하로 입력해주세요." : ""}
                onChange={handleChange}
                sx={{
                    width : "100%",
                    maxWidth : "28rem"
                }}
            />

            <LongButton text="확인" onClick={updateUserInfo}/>
        </div>
    )
}

export default EasterEgg