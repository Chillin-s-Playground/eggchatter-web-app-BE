import { create } from "zustand"

interface EasterEggState {
    nickname:string
    profile:string
    setNickname:(nickname:string) => void
    setProfile:(profile:string) => void
}

export const useEasterEggStore = create<EasterEggState>((set) => ({
    nickname : "", 
    profile : "/assets/user.png",
    setNickname: (nickname) => set({ nickname }),
    setProfile: (profile) => set({ profile }),
}))